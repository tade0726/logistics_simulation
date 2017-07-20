# -*- coding: utf-8 -*-


"""
Author: Ted
Date: 2017-07-13
des:
    main.py
"""


import simpy
from datetime import datetime
import os

t_start = datetime.now()

from src.db import *
from src.controllers import TruckController, PathGenerator
from src.utils import PipelineRecord, TruckRecord, PackageRecord
from src.vehicles import Pipeline, PipelineRes, BasePipeline
from src.machine import Unload, Presort, Cross, Hospital, SecondarySort


# log settings
import logging
logging.basicConfig(level=logging.INFO)


# todo:
# move init step into config.py

# simpy env init
env = simpy.Environment()
# raw data prepare
pipelines_table = get_pipelines()
unload_setting_dict = get_unload_setting()
reload_setting_dict = get_reload_setting()
resource_table = get_resource_limit()
equipment_resource_dict = get_resource_equipment_dict()

## c_port list
reload_c_list = list()
for _, c_list in reload_setting_dict.items():
    reload_c_list.extend(c_list)

# init trucks queues
trucks_queue = simpy.FilterStore(env)

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

# init pipelines
pipelines_dict = dict()
for _, row in pipelines_table.iterrows():
    pipeline_type = row["pipeline_type"]
    machine_type = row['machine_type']
    queue_id = row['queue_id']
    delay_time = row['process_time']
    pipeline_id = row['equipment_port_last'], row['equipment_port_next']

    if pipeline_type == "pipeline":
        pipelines_dict[pipeline_id] = Pipeline(env, delay_time, pipeline_id, queue_id, machine_type)
    else:
        pipelines_dict[pipeline_id] = PipelineRes(env,
                                                  resource_dict,
                                                  equipment_resource_dict,
                                                  delay_time,
                                                  pipeline_id,
                                                  queue_id,
                                                  machine_type)
for pipeline_id in reload_c_list:
    pipelines_dict[pipeline_id] = BasePipeline(env, machine_type="reload")

# prepare init machine dict
machine_init_dict = defaultdict(list)
for pipeline_id, pipeline in pipelines_dict.items():
    machine_init_dict[pipeline.machine_type].append(pipeline_id)

# init trucks controllers
truck_controller = TruckController(env, trucks=trucks_queue)
truck_controller.controller()

# init path generator
path_generator = PathGenerator()

# init unload machines
machines_dict = defaultdict(list)

for machine_id, truck_types in unload_setting_dict.items():
    machines_dict["unload"].append(
        Unload(env,
               machine_id=machine_id,
               unload_setting_dict=unload_setting_dict,
               reload_setting_dict=reload_setting_dict,
               trucks_q=trucks_queue,
               pipelines_dict=pipelines_dict,
               resource_dict=resource_dict,
               equipment_resource_dict=equipment_resource_dict,
               path_generator=path_generator)
    )

# init presort machines
for machine_id in machine_init_dict["presort"]:
    machines_dict["presort"].append(
        Presort(env,
                machine_id=machine_id,
                pipelines_dict=pipelines_dict,
                resource_dict=resource_dict,
                equipment_resource_dict=equipment_resource_dict,)
    )

# init cross machines
for machine_id in machine_init_dict["cross"]:
    machines_dict["cross"].append(
        Cross(
            env,
            machine_id=machine_id,
            pipelines_dict=pipelines_dict,
            resource_dict=resource_dict,
            equipment_resource_dict=equipment_resource_dict,)
    )

# init secondary_sort machines
for machine_id in machine_init_dict["secondary_sort"]:
    machines_dict["secondary_sort"].append(
        SecondarySort(
            env,
            machine_id=machine_id,
            pipelines_dict=pipelines_dict,)
    )

# init hosital machines
for machine_id in machine_init_dict["hospital"]:
    machines_dict["hospital"].append(
        Hospital(
            env,
            machine_id=machine_id,
            pipelines_dict=pipelines_dict,
            resource_dict=resource_dict,
            equipment_resource_dict=equipment_resource_dict,)
    )


# adding machines into processes
for machine_type, machines in machines_dict.items():
    logging.info(msg=f"init {machine_type} machines")
    for machine in machines:
        env.process(machine.run())

if __name__ == "__main__":

    import pandas as pd

    print("sim start..")
    env.run()

    # checking data
    truck_data = []
    for machine in machines_dict["unload"]:
        for truck in machine.done_trucks.items:
            truck_data.extend(truck.truck_data)

    pipeline_data = []
    machine_data = []

    for pipeline in pipelines_dict.values():
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

    t_end = datetime.now()
    total_time = t_end - t_start
    print(f"total time: {total_time.total_seconds()} s")