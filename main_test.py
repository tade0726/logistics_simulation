# -*- coding: utf-8 -*-


"""
Author: Ted
Date: 2017-07-13
des:
    main.py
"""


import simpy
from datetime import datetime, timedelta
import pandas as pd
import os
from collections import defaultdict

import sys
sys.path.extend(['.'])

from src.db import *
from src.controllers import TruckController, ResourceController
from src.utils import \
    (PipelineRecord, TruckRecord, PackageRecord, OutputTableColumnType, PathRecord)
from src.vehicles import Pipeline, PipelineRes, BasePipeline, SmallBag, SmallPackage, Parcel, PipelineReplace
from src.machine import *
from src.config import MainConfig, TimeConfig, LOG, SaveConfig


__all__ = ["main"]


def main():

    # start time
    t_start = datetime.now()

    # simpy env init
    env = simpy.Environment()
    # init trucks queues
    trucks_queue = simpy.FilterStore(env)
    done_trucks_queue = simpy.Store(env)

    LOG.logger_font.info("loading config data")

    # raw data prepare
    pipelines_table = get_pipelines()
    unload_setting_dict = get_unload_setting()
    reload_setting_dict = get_reload_setting()
    resource_table = get_resource_limit()
    equipment_resource_dict = get_resource_equipment_dict()
    equipment_process_time_dict = get_equipment_process_time()
    equipment_parameters = get_parameters()
    equipment_store_dict = get_equipment_store_dict()
    open_time_dict, switch_machine_names = get_equipment_timetable()

    # c_port list
    reload_c_list = list()
    for _, c_list in reload_setting_dict.items():
        reload_c_list.extend(c_list)

    # init resource
    resource_dict = defaultdict(dict)
    for _, row in resource_table.iterrows():
        resource_id = row['resource_id']
        process_time = row['process_time']
        # 设置资源为理论最大值，以便进行动态修改
        resource_max = row['resource_number']
        resource_dict[resource_id]["resource"] = simpy.PriorityResource(env=env, capacity=resource_max)
        resource_dict[resource_id]["process_time"] = process_time

    # init share_store
    share_store_dict = dict()
    for x in set(equipment_store_dict.values()):
        share_store_dict[x] = simpy.Store(env)

    # init pipelines
    pipelines_dict = dict()
    for _, row in pipelines_table.iterrows():
        pipeline_type = row["pipeline_type"]
        machine_type = row['machine_type']
        queue_id = row['queue_id']
        delay_time = row['process_time']
        pipeline_id = row['equipment_port_last'], row['equipment_port_next']

        equipment_name = row['equipment_port_next'][0]
        all_keep_open = True if equipment_name not in switch_machine_names else False

        if pipeline_type == "pipeline":
            pipelines_dict[pipeline_id] = Pipeline(env,
                                                   delay_time,
                                                   pipeline_id,
                                                   queue_id,
                                                   machine_type,
                                                   open_time_dict,
                                                   all_keep_open)

        elif pipeline_type == 'pipeline_res':
            pipelines_dict[pipeline_id] = PipelineRes(env,
                                                      resource_dict,
                                                      equipment_resource_dict,
                                                      delay_time,
                                                      pipeline_id,
                                                      queue_id,
                                                      machine_type,
                                                      equipment_process_time_dict,
                                                      open_time_dict,
                                                      all_keep_open)

        elif pipeline_type == 'pipeline_replace':
            pipelines_dict[pipeline_id] = PipelineReplace(env,
                                                          delay_time,
                                                          pipeline_id,
                                                          queue_id,
                                                          machine_type,
                                                          share_store_dict,
                                                          equipment_store_dict,
                                                          open_time_dict,
                                                          all_keep_open)
        else:
            raise ValueError("Pipeline init error!!")

    # for reload collection
    for pipeline_id in reload_c_list:
        pipelines_dict[pipeline_id] = BasePipeline(env,
                                                   pipeline_id=pipeline_id,
                                                   equipment_id=pipeline_id,
                                                   machine_type="reload")

    # for unload error
    pipelines_dict["unload_error"] = BasePipeline(env,
                                                  pipeline_id="unload_error",
                                                  equipment_id="unload_error",
                                                  machine_type="error")

    # for unload error
    pipelines_dict["error"] = BasePipeline(env,
                                           pipeline_id="error",
                                           equipment_id="error",
                                           machine_type="error")

    # for small sort bin
    pipelines_dict["small_bag_done"] = BasePipeline(env,
                                                    pipeline_id="small_bag_done",
                                                    equipment_id="small_bag_done",
                                                    machine_type="small_bag_done",
                                                    is_record=False)

    # for small_primary_error
    pipelines_dict["small_primary_error"] = BasePipeline(env,
                                                         pipeline_id="small_primary_error",
                                                         equipment_id="small_primary_error",
                                                         machine_type="error",
                                                         is_record=True)  # data will be collected

    # for small_reload_error
    pipelines_dict["small_reload_error"] = BasePipeline(env,
                                                        pipeline_id="small_reload_error",
                                                        equipment_id="small_reload_error",
                                                        machine_type="error",
                                                        is_record=True)  # data will be collected

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
                   done_trucks_q=done_trucks_queue,
                   pipelines_dict=pipelines_dict,
                   resource_dict=resource_dict,
                   equipment_resource_dict=equipment_resource_dict,
                   equipment_parameters=equipment_parameters,
                   open_time_dict=open_time_dict, )
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

    # init security machines
    for machine_id in machine_init_dict["security"]:
        machines_dict["security"].append(
            Security(
                env,
                machine_id=machine_id,
                pipelines_dict=pipelines_dict,
                resource_dict=resource_dict,
                equipment_resource_dict=equipment_resource_dict,)
        )

    # init small_primary machines
    for machine_id in machine_init_dict["small_primary"]:
        machines_dict["small_primary"].append(
            SmallPrimary(
                env,
                machine_id=machine_id,
                pipelines_dict=pipelines_dict,
                resource_dict=resource_dict,
                equipment_resource_dict=equipment_resource_dict,)
        )

    # init small_secondary machines
    for machine_id in machine_init_dict["small_secondary"]:
        machines_dict["small_secondary"].append(
            SecondarySort(
                env,
                machine_id=machine_id,
                pipelines_dict=pipelines_dict,)
        )

    # init small_reload machines
    for machine_id in machine_init_dict["small_reload"]:
        machines_dict["small_reload"].append(
            SmallReload(
                env,
                machine_id=machine_id,
                pipelines_dict=pipelines_dict,
                equipment_process_time_dict=equipment_process_time_dict,
                equipment_parameters=equipment_parameters,)
        )

    # adding machines into processes
    def setup_process_start():

        for machine_type, machines in machines_dict.items():
            LOG.logger_font.info(f"init {machine_type} machines")
            for machine in machines:
                env.process(machine.run())

        for pipeline in pipelines_dict.values():
            if isinstance(pipeline, Pipeline):
                env.process(pipeline.run())

        env.run()

    # init trucks controllers
    LOG.logger_font.info("init controllers")
    truck_controller = TruckController(env,
                                       trucks=trucks_queue,
                                       is_test=MainConfig.IS_TEST,
                                       is_parcel_only=MainConfig.IS_PARCEL_ONLY,
                                       is_land_only=MainConfig.IS_LAND_ONLY)
    truck_controller.controller()

    # init resource controller
    resource_controller = ResourceController(env,
                                             resource_dict,)
    resource_controller.controller()

    LOG.logger_font.info("init resource machine controllers..")
    LOG.logger_font.info("sim start..")

    # setup
    setup_process_start()

    num_of_trucks = len(trucks_queue.items)
    LOG.logger_font.info(f"{num_of_trucks} trucks leave in queue")
    assert num_of_trucks == 0, ValueError("Truck queue should be empty!!")

    LOG.logger_font.info("sim end..")
    LOG.logger_font.info("collecting data")

    # collecting data
    truck_data = list()
    pipeline_data = list()
    machine_data = list()
    path_data = list()

    small_bag_list = list()
    small_package_list = list()

    # truck record
    for truck in done_trucks_queue.items:
        truck_data.extend(truck.truck_data)

    # machine and pipeline records
    for pipeline in pipelines_dict.values():

        # 只有非 BasePipeline 存在 queue 和 store
        if isinstance(pipeline, BasePipeline):
            all_items = pipeline.queue.items
        else:
            all_items = pipeline.queue.items + pipeline.store.items

        for package in all_items:
            # parcel_type: {"parcel", "nc"}
            if isinstance(package, Parcel):
                machine_data.extend(package.machine_data)
                pipeline_data.extend(package.pipeline_data)
            # small package
            elif isinstance(package, SmallPackage):
                small_package_list.append(package)
            # small bag
            elif isinstance(package, SmallBag):
                small_bag_list.append(package)
            # collect path data
            path_data.extend(package.path_request_data)

    small_package_counts = 0
    # small package records
    for small_package in small_package_list:
        machine_data.extend(small_package.machine_data)
        pipeline_data.extend(small_package.pipeline_data)
        small_package_counts += 1

    for small_bag in small_bag_list:
        for small_package in small_bag.store:
            machine_data.extend(small_package.machine_data)
            pipeline_data.extend(small_package.pipeline_data)
            small_package_counts += 1

    LOG.logger_font.info(f"small_package counts: {small_package_counts}")

    truck_table = pd.DataFrame.from_records(truck_data, columns=TruckRecord._fields,)
    pipeline_table = pd.DataFrame.from_records(pipeline_data, columns=PipelineRecord._fields,)
    machine_table = pd.DataFrame.from_records(machine_data, columns=PackageRecord._fields,)
    path_table = pd.DataFrame.from_records(path_data, columns=PathRecord._fields,)

    # ------释放已经使用的对象 --------
    LOG.logger_font.info("clean memory..")
    # out
    del truck_data
    del pipeline_data
    del machine_data
    del path_data

    del small_bag_list
    del small_package_list

    # in
    del pipelines_table
    del unload_setting_dict
    del reload_setting_dict
    del resource_table
    del equipment_resource_dict
    del equipment_process_time_dict
    del equipment_parameters
    del equipment_store_dict
    del open_time_dict
    del switch_machine_names

    # process data
    del machine_init_dict
    del machines_dict
    del pipelines_dict
    del resource_dict

    del reload_c_list
    del share_store_dict

    # class instance
    del truck_controller
    del resource_controller

    # ------释放已经使用的对象 --------

    if not os.path.isdir(SaveConfig.OUT_DIR):
        os.makedirs(SaveConfig.OUT_DIR)

    # process data
    LOG.logger_font.info(msg="processing data")
    # time stamp for db
    db_insert_time = t_start

    def add_time(table: pd.DataFrame):
        """添加仿真的时间戳， 以及运行的日期"""
        table["real_time_stamp"] = table["time_stamp"].apply(lambda x: TimeConfig.ZERO_TIMESTAMP + timedelta(seconds=x))
        table["run_time"] = db_insert_time
        return table

    truck_table = add_time(truck_table)
    pipeline_table = add_time(pipeline_table)
    machine_table = add_time(machine_table)
    path_table["run_time"] = db_insert_time

    # output data
    LOG.logger_font.info("output data")

    # output machine table only
    if MainConfig.OUTPUT_MACHINE_TABLE_ONLY:
        if MainConfig.SAVE_LOCAL:
            write_local('machine_table', machine_table)
        else:
            write_mysql("machine_table", machine_table, OutputTableColumnType.package_columns)

    else:
        if MainConfig.SAVE_LOCAL:
            write_local('machine_table', machine_table)
            write_local('pipeline_table', pipeline_table)
            write_local('truck_table', truck_table)
            write_local('path_table', path_table)
        else:
            write_mysql("machine_table", machine_table, OutputTableColumnType.package_columns)
            write_mysql("pipeline_table", pipeline_table, OutputTableColumnType.pipeline_columns)
            write_mysql("truck_table", truck_table, OutputTableColumnType.truck_columns)
            write_mysql('path_table', path_table, OutputTableColumnType.path_columns)

    t_end = datetime.now()
    total_time = t_end - t_start

    LOG.logger_font.info(f"total time: {total_time.total_seconds()} s")


if __name__ == '__main__':
    main()