# -*- coding: utf-8 -*-


"""
Author: Ted
Date: 2017-07-13
des:
    main.py
"""


# log settings
import logging
logging.basicConfig(level=logging.INFO)

import simpy
from datetime import datetime, timedelta
import os
from collections import defaultdict

from simpy_lib.hangzhou_simpy.src.db import *
from simpy_lib.hangzhou_simpy.src.controllers import TruckController
from simpy_lib.hangzhou_simpy.src.utils \
    import PipelineRecord, TruckRecord, PackageRecord
from simpy_lib.hangzhou_simpy.src.vehicles \
    import Pipeline, PipelineRes, BasePipeline
from simpy_lib.hangzhou_simpy.src.machine \
    import Unload, Presort, Cross, Hospital, SecondarySort
from simpy_lib.hangzhou_simpy.src.config import MainConfig
from simpy_lib.hangzhou_simpy.src.config import TimeConfig

from tkinter import NORMAL, DISABLED, END

__all__ = ["main"]

# todo: add parameters

def main(run_arg):

    # start time
    t_start = datetime.now()

    # simpy env init
    env = simpy.Environment()
    # init trucks queues
    trucks_queue = simpy.FilterStore(env)
    # =============================== 测试日志输出 ==============================
    # text_txt_receipt['state'] = NORMAL
    # text_txt_receipt.delete('1.0', END)
    # print('loading config data=====', text_txt_receipt)
    # text_txt_receipt.insert(END, "loading config data\n")
    # text_txt_receipt['state'] = DISABLED
    # ==========================================================================
    logging.info("loading config data")

    # raw data prepare
    pipelines_table = get_pipelines()
    unload_setting_dict_src = get_unload_setting()
    reload_setting_dict = get_reload_setting()
    resource_table = get_resource_limit()
    equipment_resource_dict = get_resource_equipment_dict()
    equipment_process_time_dict = get_equipment_process_time()
    equipment_parameters = get_parameters()
    equipment_on_list, equipment_off_list = get_equipment_on_off()

    # init trucks controllers
    logging.info("loading package data")
    truck_controller = TruckController(env,
                                       trucks=trucks_queue,
                                       is_test=MainConfig.IS_TEST,
                                       is_parcel_only=MainConfig.IS_PARCEL_ONLY,
                                       is_land_only=MainConfig.IS_LAND_ONLY)
    truck_controller.controller()

    # equipment setting from unload
    unload_setting_dict = {key: val for key, val in unload_setting_dict_src.items() if key in equipment_on_list}

    # c_port list
    reload_c_list = list()
    for _, c_list in reload_setting_dict.items():
        reload_c_list.extend(c_list)

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

    for pipeline_id in reload_c_list:
        pipelines_dict[pipeline_id] = BasePipeline(env,
                                                   pipeline_id=pipeline_id,
                                                   equipment_id=pipeline_id,
                                                   machine_type="reload")

    pipelines_dict["unload_error_packages"] = BasePipeline(env,
                                                           pipeline_id="unload_error",
                                                           equipment_id="unload_error",
                                                           machine_type="error")

    # prepare init machine dict
    machine_init_dict = defaultdict(list)
    for pipeline_id, pipeline in pipelines_dict.items():
        machine_init_dict[pipeline.machine_type].append(pipeline_id)


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

    # init hospital machines
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
        logging.info(f"init {machine_type} machines")
        for machine in machines:
            env.process(machine.run())

    logging.info("sim start..")
    env.run()
    logging.info("sim end..")
    logging.info("collecting data")

    # checking data
    truck_data = []
    pipeline_data = []
    machine_data = []

    for machine in machines_dict["unload"]:
        for truck in machine.done_trucks.items:
            truck_data.extend(truck.truck_data)

    for pipeline in pipelines_dict.values():
        for package in pipeline.queue.items:
            pipeline_data.extend(package.pipeline_data)
            machine_data.extend(package.machine_data)

    truck_table = pd.DataFrame.from_records(truck_data, columns=TruckRecord._fields,)
    pipeline_table = pd.DataFrame.from_records(pipeline_data, columns=PipelineRecord._fields,)
    machine_table = pd.DataFrame.from_records(machine_data, columns=PackageRecord._fields,)

    if not os.path.isdir(SaveConfig.OUT_DIR):
        os.makedirs(SaveConfig.OUT_DIR)

    # process data
    logging.info(msg="processing data")
    # time stamp for db
    db_insert_time = run_arg

    def add_time(table: pd.DataFrame):
        """添加仿真的时间戳， 以及运行的日期"""
        table["real_time_stamp"] = table["time_stamp"].apply(lambda x: TimeConfig.ZERO_TIMESTAMP + timedelta(seconds=x))
        table["run_time"] = db_insert_time
        return table

    truck_table = add_time(truck_table)
    pipeline_table = add_time(pipeline_table)
    machine_table = add_time(machine_table)

    # output data
    logging.info("output data")

    if MainConfig.SAVE_LOCAL:
        write_local('machine_table', machine_table)
        write_local('pipeline_table', pipeline_table)
        write_local('truck_table', truck_table)
    else:
        write_mysql("pipeline_table", pipeline_table)
        write_mysql("truck_table", truck_table)
        write_mysql("machine_table", machine_table)

    t_end = datetime.now()
    total_time = t_end - t_start

    logging.info(f"total time: {total_time.total_seconds()} s")


if __name__ == '__main__':
    pass
    # main()