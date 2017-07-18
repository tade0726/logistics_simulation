# -*- coding: utf-8 -*-


"""
author: Ted
date: 2017-07-11
des:

unload modules
"""
import simpy
from collections import defaultdict
from src.vehicles import Package
import random
from src.controllers.paths import path_generator

# todo: wait for yuanfang
from src.controllers import paths

TRUCK_CONVERT_TIME = 300


class Unload:

    def __init__(self,
                 env: simpy.Environment,
                 machine_id: str,
                 equipment_id: str,
                 unload_setting_dict: dict,
                 reload_setting_dict: dict,
                 trucks_q: simpy.FilterStore,
                 pipelines_dict: defaultdict,
                 resource_dict: defaultdict
                 ):

        self.env = env
        self.machine_id = machine_id
        self.equipment_id = equipment_id
        self.truck_types = unload_setting_dict[equipment_id]
        self.reload_setting_dict = reload_setting_dict
        self.trucks_q = trucks_q
        self.pipelines_dict = pipelines_dict
        self.resource = resource_dict[equipment_id]
        self.process_time = resource_dict['process_time']

        self.num_of_truck = 0
        self.packages_processed = dict()
        self.done_trucks = simpy.Store(env)

        # store data
        self.package_records = []
        self.truck_records = []

    def process_package(self, process_idx, package: Package):

        with self.resource.request() as req:
            yield req
            next_pipeline = package.next_pipeline

            package.start_serve()
            package.add_machine_id(self.machine_id)

            yield self.env.timeout(self.process_time)
            package.end_serve()

            self.pipelines_dict[next_pipeline].put(package)
            self.packages_processed[process_idx].succeed()

            self.package_records.append(package.package_record)

    def run(self):

        while True:
            # filter out the match truck(LL/LA/AL/AA)
            truck = yield self.trucks_q.get(lambda x: x.truck_type in self.truck_types)
            # add data
            truck.start_serve()
            truck.add_machine_id(machine_id=self.machine_id)

            # init packages_processed empty
            self.packages_processed = dict()

            for process_idx, package_record in truck.store.itterrows():

                package_start = self.machine_id
                # building key
                reload_key = (package_record["dest_code"], "L", "reload")
                # look up the c-port for different destination
                package_ends = self.reload_setting_dict.get(reload_key)
                # random choice if package_ends more than 1
                package_end = random.choice(package_ends)
                # init package
                package = Package(env=self.env,
                                  attr=package_record,
                                  path=path_generator(package_start, package_end))
                # package add data
                package.start_wait()
                package.add_machine_id(self.machine_id)
                # need request resource for processing
                self.packages_processed[process_idx] = self.env.event()
                self.env.process(self.process_package(process_idx, package))

            # all the package are processed
            yield self.env.all_of(self.packages_processed.values())
            # truck add data
            truck.end_serve()
            self.truck_records.append(truck.truck_record)
            # truck is out
            self.done_trucks.put(truck)
            # truck convert time
            yield self.env.timeout(TRUCK_CONVERT_TIME)
            self.num_of_truck += 1




