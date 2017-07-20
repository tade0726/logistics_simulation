# -*- coding: utf-8 -*-

"""
==================================================================================================================================================
                                                     杭州HUB仿真项目

                                    项目启动日期：2017年7月6日
                                    项目启动标识：AIRPORT OF EZHOU'S PROJECT  -- HZ
                                    ===========================================
                                    代码创建日期：2017年7月6日
                                    代码创建工程师：韩蓝毅
                                    代码版本：1.0
                                    版本更新日期：2017年7月6日
                                    版本更新工程师：韩蓝毅

                                    代码整体功能描述：终分拣模块，
                                                      1、终分拣模拟



==================================================================================================================================================
"""

import simpy
import random
from src.db import *
from src.vehicles.items import Package
from src.machine.secondary_sort import SecondarySort
from src.vehicles import Pipeline


RANDOM_SEED = 42
CART_NUM = 300
MACHINE_ID = ["i2-1"]
DEST_NUM = 50
DEST_ID = {}
ALL_PACKAGES = {}
INPUT_QUEUE_DICT = {}
OUTPUT_QUEUE_DICT = {}
random.seed(RANDOM_SEED)


# 生成出口编号
def generate_dest_id():
    dest_list = []
    for mid in MACHINE_ID:
        DEST_ID[mid] = []
        for i in range(DEST_NUM):
            DEST_ID[mid].append(mid.replace("i", "c")[0:3] + str(i))
        dest_list += DEST_ID[mid]
    return dest_list


# 生成货物的process
def generate_package(env, mid):
    package_queue = INPUT_QUEUE_DICT[mid]
    interval = random.randint(2, 10)
    for i in range(random.randint(100, 200)):
        yield env.timeout(interval)
        dest_id = random.choice(DEST_ID[mid])
        path = (mid, dest_id)
        item = Package(env, attr=None, item_id=f'{mid}-{i+1}', path=path)
        item.next_pipeline = path
        item.pipeline_data.append((path[0], env.now))
        package_queue.put(item)


if __name__ == '__main__':
    print("start")

    dest_id_list = generate_dest_id()

    machine_dict = {}
    env = simpy.Environment()

    # 生成输入和输出队列
    for mid in MACHINE_ID:
        INPUT_QUEUE_DICT[mid] = simpy.Store(env)
    for did in dest_id_list:
        OUTPUT_QUEUE_DICT[did] = simpy.Store(env)

    # 生成pipeline
    pipelines_table = get_pipelines(is_filter=False)
    pipelines_dict = dict()
    for _, row in pipelines_table.iterrows():
        machine_type = row['machine_type']
        queue_id = row['queue_id']
        delay_time = row['process_time']
        pipeline_id = row['equipment_port_last'], row['equipment_port_next']
        pipelines_dict[pipeline_id] = Pipeline(env, delay_time, pipeline_id,
                                               queue_id, machine_type)

    for mid in MACHINE_ID:
        cou = 1
        count = str(cou)
        env.process(generate_package(env, mid))
        input_queue = INPUT_QUEUE_DICT[mid]
        time = 10
        secondary_sort_machine = SecondarySort(env,
                                               count,
                                               time,
                                               CART_NUM,
                                               pipelines_dict=pipelines_dict,
                                               input_queue=input_queue,
                                               output_queue=OUTPUT_QUEUE_DICT)
        machine_dict[mid] = secondary_sort_machine
        env.process(secondary_sort_machine.run())
        cou += 1

    env.run()
    print("End.")