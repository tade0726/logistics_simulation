# -*- coding: utf-8 -*-


"""
Author: Ted
Date: 2017-07-13
des:
    main.py
"""


import simpy

from src.db import *
from src.controllers import TruckController, PathGenerator
from src.vehicles import Pipeline
from src.machine import Unload


# todo:
# move init step into config.py

# simpy env init
env = simpy.Environment()
# raw data prepare
pipelines_table = get_pipelines(is_filter=False)
unload_setting_dict = get_unload_setting()
reload_setting_dict = get_reload_setting()
resource_table = get_resource_limit()
equipment_resource_dict = get_resource_equipment_dict()

# init trucks queues
trucks_queue = simpy.FilterStore(env)

# init pipeline
pipelines_dict = dict()
for _, row in pipelines_table.iterrows():
    machine_type = row['machine_type']
    queue_id = row['queue_id']
    delay_time = row['process_time']
    pipeline_id = row['equipment_port_last'], row['equipment_port_next']
    pipelines_dict[pipeline_id] = Pipeline(env, delay_time, pipeline_id, queue_id, machine_type)

# init resource
resource_dict = defaultdict(dict)
for _, row in resource_table.iterrows():
    resource_id = row['resource_id']
    process_time = row['process_time']
    resource_limit = row['resource_limit']
    # add info
    if resource_limit:
        resource_dict[resource_id]["resource"] = simpy.Resource(env=env, capacity=resource_limit)
        resource_dict[resource_id]["process_time"] = process_time

# init trucks controllers
truck_controller = TruckController(env, trucks=trucks_queue)
truck_controller.controller()

# init path generator
path_generator = PathGenerator()

# init unload machines
machines = []
# todo
for machine_id, truck_types in unload_setting_dict.items():
    machines.append(Unload(env,
                           machine_id=machine_id,
                           equipment_id=machine_id,
                           unload_setting_dict=unload_setting_dict,
                           reload_setting_dict=reload_setting_dict,
                           trucks_q=trucks_queue,
                           pipelines_dict=pipelines_dict,
                           resource_dict=resource_dict,
                           equipment_resource_dict=equipment_resource_dict,
                           path_generator=path_generator))

# adding machine into processes
for machine in machines:
    env.process(machine.run())

if __name__ == "__main__":
    import pandas as pd
    from datetime import datetime

    t_start = datetime.now()

    print("sim start..")
    env.run(10000)

    t_end = datetime.now()

    # checking data
    package_data = []
    truck_data = []
    for machine in machines:
        package_data.extend(machine.package_records)
        truck_data.extend(machine.truck_records)

    total_time = t_end - t_start

    print(f"total time: {total_time.total_seconds()} s")

    package_table = pd.DataFrame.from_records(package_data)
    truck_table = pd.DataFrame.from_records(truck_data)

    package_table.to_csv(join(SaveConfig.DATA_DIR, "package_records.csv"), index=0)
    truck_table.to_csv(join(SaveConfig.DATA_DIR, "truck_table.csv"), index=0)
