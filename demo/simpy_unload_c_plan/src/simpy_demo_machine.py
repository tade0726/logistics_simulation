# -*- coding: utf-8 -*-


"""
author: Ted
date: 2017-06-13
des:

demo of unload module
"""

# todo: monitor how many item being process per second by each machine
# todo: using mongodb for record store


import random
import simpy
import pandas as pd


# for machine 
import re
from src.config.io_rule import choiceW
from src.config.io_rule import (r_dock_s_road_rule, r_dock_unload, )
from src.config.queues import (s_road_q, s_int_q, s_domestic_q)
from src.config.io_rule import (city_apt, apt_reload,r_dock_r_presort_infeed_rule, r_presort_infeed_rule)

# init queue
from src.config.queues import (r_presort_infeed_q, i_presort_infeed_q, d_presort_infeed_q)
from src.config.queues import (r_reload_q, i_reload_q, d_reload_q)

# dist
from src.config.dist import (nc_dist, irregular_dist, r_dock_dist, r_dock_r_presort_dist,)

def check_truck_empty(env, trucks: simpy.PriorityStore, truck_empty: simpy.Event):
    while True:
        if not trucks.items:
            truck_empty.succeed()
        yield env.timeout(100)

def truck_come_controller(trucks: simpy.PriorityStore, trucks_dict: dict):
    """
    :param env: from simpy
    :param trucks: a queue (FIFO)
    :param trucks_dict: a dict contain dataframe, {(truck_id, come_time): df1, (truck_id, come_time): df2, ...}
    :return:
    des: put truck into trucks, at 0s
    """

    for truck_key in trucks_dict.keys():
        (truck_id, come_time) = truck_key
        trucks.put(simpy.PriorityItem(
            priority=come_time,
            item=Truck(truck_id=truck_id,
                       come_time=come_time,
                       packages=trucks_dict[truck_key]))
        )


class Package:

    def __init__(self, attr, now_position: str=None, next_position: str=None):
        """
        :param attr: package records
        :param now_position: position of last machine(pipeline)
        :param next_position: position of next machine(pipeline)
        """
        # using for pipeline length calculations
        self.now_position = now_position
        self.next_position = next_position

        self.attr = attr
        self.check = False
        self.customs = False

        # record of the path of the package,
        # element will be a dict {'now_position': 'some where', 'next_position', 'some where', 'last_timestamp': 1000}
        self.path = []

    def __str__(self):
        """
        :return:
        """
        display_dct = dict(self.attr)
        display_dct['check'] = self.check
        display_dct['customs'] = self.customs

        return f"<package attr:{dict(display_dct)}>"

# vehicles


class Truck:

    def __init__(self, truck_id, come_time, packages:pd.DataFrame):
        """
        :param truck_id: self explain
        :param come_time: self explain
        :param packages: a dataframe contain all packages
        """
        self.truck_id = truck_id
        self.come_time = come_time
        self.store = packages

    def __str__(self):
        """
        :return:
        """
        return f"<truck_id: {self.truck_id}, come_time: {self.come_time}, store_size:{len(self.store)}>"


class Uld:
    pass


# machine

class UnloadR:

    def __init__(self, machine_id, last_queue, env, logger,):

        self.machine_id = machine_id
        self.last_queue = last_queue
        self.env = env
        self.num_of_truck = 0

        # parameters
        self.drive = 5 * 60
        self.con_belt_speed = 1 * 1000  # notes: the length of dist in dist table are recorded as (mm)
        self.nc_speed = 2 * 1000  # notes: the length of dist in dist table are recorded as (mm)
        self.ir_speed = 2 * 1000  # notes: the length of dist in dist table are recorded as (mm)
        self.unload_efficiency = 3.6  # request a package every 3.6s

        # some re for in_out name
        self.re_reload = re.compile(r"Reload_\w\d")

        # 3 ways out
        self.r_small_queue = s_road_q
        self.i_small_queue = s_int_q
        self.d_small_queue = s_domestic_q

        self.r_presort_infeed_queue = r_presort_infeed_q
        self.i_presort_infeed_queue = i_presort_infeed_q
        self.d_presort_infeed_queue = d_presort_infeed_q

        self.r_reload_queue = r_reload_q
        self.i_reload_queue = i_reload_q
        self.d_reload_queue = d_reload_q

        #io rules
        self.r_dock_unload = r_dock_unload
        self.r_dock_s_road = r_dock_s_road_rule
        self.apt_reload = apt_reload
        self.city_apt = city_apt

        self.r_dock_r_presort_infeed_rule = r_dock_r_presort_infeed_rule
        self.r_presort_infeed_rule = r_presort_infeed_rule

        # dist
        self.r_dock_dist = r_dock_dist
        self.nc_dist = nc_dist
        self.r_dock_r_presort_dist = r_dock_r_presort_dist
        # logger
        self.log_record = logger(log_name=f"record_{self.machine_id}")
        self.log_error = logger(log_name=f"error_{self.machine_id}")
        # queue for checking and customs
        self.tmp_queue = simpy.PriorityStore(self.env)
        # queue for all item
        self.wait_queue = simpy.PriorityStore(self.env)
        # event of empty
        self.empty = self.env.event()
        # init process
        # fixme: how many check and customs personals?
        for i in range(100):
            self.env.process(self.check_and_customs(name = f"checker_{i}"))
        self.env.process(self.sorter())
        self.env.process(self.empty_queue())

    def empty_queue(self):
        while True:
            if not self.tmp_queue.items and not self.wait_queue.items:
                self.empty.succeed()
                self.empty = self.env.event()
            yield self.env.timeout(100)

    def check_and_customs(self, name):
        """
        :param name: a name for single process
        :return:
        des:
            package needed to be added time will be deal here
        """
        name = name
        while True:
            package = yield self.tmp_queue.get()
            package = package.item
            if package.check:
                yield self.env.timeout(1800)
            if package.customs:
                yield self.env.timeout(3600)
            self.wait_queue.put(simpy.PriorityItem(self.env.now, package))

    def sorter(self):
        """
        :return:
        des:
            package send to reload, will be sort
        """
        while True:
            package = yield self.wait_queue.get()
            package = package.item
            destination = package.attr['destination_city']
            now_position = self.r_dock_unload.get(self.machine_id, None)
            package.now_position = now_position
            try:
                # fixme: The length of pipeline to next machine should not count here
                # go to reload
                if package.attr['pcs_type'] in ["NC", "irregular"]:

                    # convert destination for Domestic
                    if package.attr['destination_type'] == 'D':
                        destination = self.city_apt.get(destination)

                    next_position = choiceW(self.apt_reload, destination)
                    package.next_position = next_position

                    path_record = dict(
                        now_position=package.now_position,
                        next_position=package.next_position,
                        last_timestamp=self.env.now,)

                    package.path.append(path_record)

                    if package.attr["destination_type"] in ["I", "INF"]:
                        self.i_reload_queue[next_position].put(simpy.PriorityItem(self.env.now, package))
                        # for test log fixme
                        self.log_record.info(f"package: {package} go to {package.next_position} at time {self.env.now}")

                    elif package.attr["destination_type"] == "R":
                        self.r_reload_queue[next_position].put(simpy.PriorityItem(self.env.now, package))
                        # for test log fixme
                        self.log_record.info(f"package: {package} go to {package.next_position} at time {self.env.now}")

                    elif package.attr["destination_type"] == "D":
                        self.d_reload_queue[next_position].put(simpy.PriorityItem(self.env.now, package))
                        # for test log fixme
                        self.log_record.info(f"package: {package} go to {package.next_position} at time {self.env.now}")

                    else:
                        pass

                # go to small
                elif package.attr['pcs_type'] == "small":
                    next_position = self.r_dock_s_road.get(self.machine_id, None)
                    package.next_position = next_position

                    path_record = dict(
                        now_position=package.now_position,
                        next_position=package.next_position,
                        last_timestamp=self.env.now,)

                    package.path.append(path_record)

                    self.r_small_queue[next_position].put(simpy.PriorityItem(self.env.now, package))
                    # for test log fixme
                    self.log_record.info(f"package: {package} go to {package.next_position} at time {self.env.now}")

                # go to presort infeed
                else:
                    next_position = self.r_dock_r_presort_infeed_rule[self.machine_id]
                    package.next_position = next_position

                    path_record = dict(
                        now_position=package.now_position,
                        next_position=package.next_position,
                        last_timestamp=self.env.now,)

                    package.path.append(path_record)

                    self.r_presort_infeed_queue[next_position].put(simpy.PriorityItem(self.env.now, package))
                    # for test log fixme
                    self.log_record.info(f"package: {package} go to {package.next_position} at time {self.env.now}")

            except Exception as exc:
                self.log_error.info(f"package: {package}, error: {exc}")

    def run(self):

        while True:

            # add truck moving time
            if self.num_of_truck > 0:
                add_time = \
                    self.drive + self.r_dock_dist[self.machine_id] / self.con_belt_speed
                yield self.env.timeout(add_time)

            truck = yield self.last_queue.get()
            truck = truck.item

            print(f"Get a truck: {truck.truck_id} at {self.env.now}, truck_num: "
                  f"{self.num_of_truck}, machine_id: {self.machine_id}")

            for _, package_record in truck.store.iterrows():
                # request package every 3.6s
                yield self.env.timeout(self.unload_efficiency)

                package = Package(attr=package_record)
                probra_check = random.random()
                probra_customs = random.random()

                if probra_check <= 0.05:
                    package.check = True
                if probra_customs <= 0.05:
                    package.customs = True
                if probra_check or probra_customs:
                    self.tmp_queue.put(simpy.PriorityItem(self.env.now, package))
                else:
                    self.wait_queue.put(simpy.PriorityItem(self.env.now, package))

            self.num_of_truck += 1


class PresortInfeed:
    pass


class Presort:
    pass


class PresortOutlet:
    pass


class SecondaryInfeed:
    pass


class Secondary:
    pass


class SecondaryOutlet:
    pass


class SmallModule:
    pass


class Reload:
    pass

