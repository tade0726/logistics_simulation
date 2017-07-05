# -*- coding: utf-8 -*-


"""
author: Ted
date: 2017-06-22
des:

main for whole simulation
"""

import simpy
from simpy import AllOf
from src.config.io_rule import r_dock_unload
from src.config.queues import env
from src.simpy_demo_machine import UnloadR, truck_come_controller, check_truck_empty
from src.tools.db import get_trucks
from src.tools.loggers import get_logger

from datetime import datetime

if __name__ == '__main__':
    # timer for real time
    t1 = datetime.now()
    # a Environment instance
    env = env
    # init trucks queue
    trucks_dict = get_trucks(istest=False)
    trucks = simpy.PriorityStore(env)
    # truck controller : putting trucks
    truck_come_controller(trucks, trucks_dict)
    # loading r_unload machines
    machine_dict = {}
    for machine_id in r_dock_unload.keys():

        unload_machine = UnloadR(machine_id=machine_id,
                                 last_queue=trucks,
                                 env=env,
                                 logger=get_logger,)

        machine_dict[machine_id] = unload_machine
        # add process
        env.process(unload_machine.run())
    # truck empty event and machine empty events
    truck_empty = env.event()
    stop_event = \
        AllOf(env, [machine.empty for _, machine in machine_dict.items()] + [truck_empty])
    # add controller
    env.process(check_truck_empty(env, trucks, truck_empty))
    # simulator begin
    env.run(stop_event)
    # timer for real time
    t2 = datetime.now()
    total_time = t2 - t1
    t1_str = t1.strftime("%H:%M:%S")
    print(f"Total time: {total_time.seconds} s, start at: {t1_str}")