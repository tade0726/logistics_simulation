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
from src.utils import PipelineRecord, TruckRecord, PackageRecord
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
    import os

    t_start = datetime.now()

    print("sim start..")
    env.run()
    t_end = datetime.now()
    # checking data
    truck_data = []

    for machine in machines:
        for truck in machine.done_trucks.items:
            truck_data.extend(truck.truck_data)

    total_time = t_end - t_start

    print(f"total time: {total_time.total_seconds()} s")

    presort_pipelines = list(
        filter(lambda x: True if x.machine_type == "presort" else False, pipelines_dict.values())
    )

    pipeline_data = []
    machine_data = []

    for pipeline in presort_pipelines:
        for package in pipeline.queue.items:
            pipeline_data.extend(package.pipeline_data)
            machine_data.extend(package.machine_data)

    truck_table = pd.DataFrame.from_records(truck_data, columns=TruckRecord._fields,)
    pipeline_table = pd.DataFrame.from_records(pipeline_data, columns=PipelineRecord._fields,)
    machine_table = pd.DataFrame.from_records(machine_data, columns=PackageRecord._fields,)

    if not os.path.isdir(SaveConfig.OUT_DIR):
        os.makedirs(SaveConfig.OUT_DIR)

    truck_table.to_csv(join(SaveConfig.OUT_DIR, "truck_table.csv"), index=0)
    pipeline_table.to_csv(join(SaveConfig.OUT_DIR, "pipeline_table.csv"), index=0)
    machine_table.to_csv(join(SaveConfig.OUT_DIR, "machine_table.csv"), index=0)