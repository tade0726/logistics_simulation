# -*- coding: utf-8 -*-

"""
author: Ted
date: 2017-06-13
des:

demo of unload module

now using good as a process

"""

# todo: how to add info of machine into resource
# todo: presort infeed has a capacity



import random
import simpy



class MachineConfigBase:

    SPEED = 1
    NC_SPEED = 2
    IR_SPEED = 2



class Machine:

    def __init__(self, env, id, dock_name, machine_name, capacity=None):

        """
        :param env: env from simPy
        :param id: machine id
        :param dock_name: dock R/I/D
        :param machine_name: unload/presort/secondary/S/reload
        :param capacity: the capacity of the Machine
        """
        self.machine_id = id
        self.dock_name = dock_name
        self.machine_name = machine_name

        if capacity:
            self.capacity = simpy.Resource(env=env, capacity=capacity)



class Package:

    def __init__(self, good_id, from_w, env, arrive_time, attr:dict, io_rules):

        self.good_id = good_id
        self.from_w = from_w
        self.env = env
        self.arrive_time = arrive_time
        self.attr = attr
        self.io_rules = io_rules

    def unload(self, ms):
        # todo: add logic
        # package arrive time
        yield self.env.timeout(self.arrive_time)
        print(f"good {self.good_id} arrive at {self.env.now}")
        machine = yield ms.get(lambda machine: machine.machine_name == 'unload')
        # todo add process
        # 1. checking & customs
        probra_chk = random.uniform(0,100)  # 0<= x <100, float
        probra_cutms = random.uniform(0,100)  # 0<= x <100, float

        if probra_chk <= 0.05:
            yield self.env.timeout(1800)
        if probra_cutms <= 0.02:
            yield self.env.timeout(3600)


        yield ms.put(machine)


    def pre_sort_infeed(self):
        pass

    def pre_sort(self):
        pass

    def pre_sort_outlet(self):
        pass

    def second_sort_infeed(self):

    def second_sort(self):
        pass

    def second_sort_outlet(self):
        pass

    def s_module(self):
        pass

    def reload(self):
        pass

    def run(self, ms):

        self.unload(ms)




if __name__ == "__main__":

    env = simpy.Environment()

    # todo: lots of machine need to instanced

    # no capacity
    m1 = Machine(id='R_dock1', dock_name='R', machine_name='unload',)
    # with capacity
    m2 = Machine(id='R_presort_infeed_10', dock_name='R',
                 machine_name='preosrt_infeed',
                 capacity=12)

    machines = simpy.FilterStore(env)
    machines.items = [m1, m2]

    packages = [Package(good_id=i, env=env, arrive_time= i * 3) for i in range(30)]

    for package in packages:
        env.process(package.unload(machines))

    env.run()

