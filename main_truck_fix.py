# -*- coding: utf-8 -*-


"""
Author: Ted
Date: 2017-08-09
des:
    a test file for trucks
"""

import simpy
from collections import defaultdict
from src.db import *
from src.machine import Unload
from src.vehicles import Pipeline, PipelineRes, BasePipeline
from src.config import *
from src.controllers import TruckController

# simpy env init
env = simpy.Environment()
# init trucks queues
trucks_queue = simpy.FilterStore(env)

# raw data prepare
pipelines_table = get_pipelines()
unload_setting_dict = get_unload_setting()
reload_setting_dict = get_reload_setting()
resource_table = get_resource_limit()
equipment_resource_dict = get_resource_equipment_dict()
equipment_process_time_dict = get_equipment_process_time()
equipment_parameters = get_parameters()
equipment_on_list, equipment_off_list = get_equipment_on_off()

# init resource and pipeline
resource_dict = defaultdict(dict)
for _, row in resource_table.iterrows():
    resource_id = row['resource_id']
    process_time = row['process_time']
    # fixme: temp change
    # resource_limit = row['resource_limit']
    resource_limit = row['resource_number']
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
    elif pipeline_type == 'pipeline_res':
        pipelines_dict[pipeline_id] = PipelineRes(env,
                                                  resource_dict,
                                                  equipment_resource_dict,
                                                  delay_time,
                                                  pipeline_id,
                                                  queue_id,
                                                  machine_type,
                                                  equipment_process_time_dict)
    else:
        raise ValueError("Pipeline init error!!")


# for unload error
pipelines_dict["unload_error"] = BasePipeline(env,
                                              pipeline_id="unload_error",
                                              equipment_id="unload_error",
                                              machine_type="error")

# init truck queue
truck_controller = TruckController(env,
                                   trucks=trucks_queue,
                                   is_test=MainConfig.IS_TEST,
                                   is_parcel_only=MainConfig.IS_PARCEL_ONLY,
                                   is_land_only=MainConfig.IS_LAND_ONLY)

truck_controller.controller()

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
               equipment_parameters=equipment_parameters)
    )

# adding machines into processes
for machine_type, machines in machines_dict.items():
    LOG.logger_font.info(f"init {machine_type} machines")
    for machine in machines:
        env.process(machine.run())

env.run()

assert len(trucks_queue.items) == 0, "truck_queue should be empty!!"