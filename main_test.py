# -*- coding: utf-8 -*-


"""
Author: Ted
Date: 2017-07-13
des:
    main.py
"""


import simpy
import pandas as pd
from collections import defaultdict

from src.db import get_trucks, get_pipelines, get_unload_setting, get_resource_limit, get_reload_setting
from src.controllers import truck_controller
from src.vehicles import Pipeline
from src.machine import Unload


# todo:
# move init step into config.py

# simpy env init
env = simpy.Environment()

# raw data prepare
trucks_dict = get_trucks(is_local=True)
pipelines_table = get_pipelines(is_local=True)
unload_setting_dict = get_unload_setting(is_local=True)
reload_setting_dict = get_reload_setting(is_local=True)
resource_table = get_resource_limit(is_local=True)

# init trucks queues
trucks_queue = simpy.FilterStore(env)

# init pipeline
pipelines_dict = defaultdict(dict)
for _, row in pipelines_table.iterrows():
    machine_type = row['machine_type']
    queue_id = row['queue_id']
    delay_time = row['process_time']
    pipeline_id = row['equipment_port_last'], row['equipment_port_next']
    pipelines_dict[machine_type][pipeline_id] = Pipeline(env, delay_time, pipeline_id, queue_id, machine_type)

# init resource
resource_dict = defaultdict(dict)
for _, row in resource_table.iterrows():
    equipment_id = row['equipment_id']
    process_time = row['process_time']
    resource_limit = row['resource_limit']
    # add info
    resource_dict[equipment_id]["resource"] = simpy.Resource(env=env, capacity=resource_limit)
    resource_dict[equipment_id]["process_time"] = process_time

# init trucks controllers
env.process(truck_controller(env, trucks_queue))

# todo
# init unload machines
machines = []
# todo
for machine_id, truck_types in unload_setting_dict.items():
    machines.append(Unload(env, machine_id, machine_id, unload_setting_dict,
                           reload_setting_dict, trucks_queue, pipelines_dict,
                           resource_dict, ))

env.run()