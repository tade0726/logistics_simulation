# -*- coding: utf-8 -*-

"""
======================================================================================================
                                                     杭州HUB仿真项目

                                    项目启动日期：2017年7月6日
                                    项目启动标识：AIRPORT OF EZHOU'S PROJECT  -- HZ
                                    ===========================================
                                    代码创建日期：2017年7月13日
                                    代码创建工程师：谈和
                                    代码版本：1.0
                                    版本更新日期：2017年7月6日
                                    版本更新工程师：谈和

                                    代码整体功能描述：测试hospital模块；


=====================================================================================================
"""

import simpy
import random
from src.machine.hospital.hospital import Hospital
from src.vehicles.items import Package, Pipeline

# from src.vehicles.items import Package

RANDOM_SEED = 42
WORKER_NUM = 2
MACHINE_ID = ["h1-1", "h2-1", "h3-1", "h3-2", "h3-3", "h3-4"]
DEST_NUM = 3
DEST_ID = {
    "h1-1": "x8-1",
    "h2-1": "x9-1",
    "h3-1": "x12-1",
    "h3-2": "x11-1",
    "h3-3": "x13-1",
    "h3-4": "x14-1"
}
ALL_PACKAGES = {}
INPUT_QUEUE_DICT = {}
OUTPUT_QUEUE_DICT = {}
random.seed(RANDOM_SEED)


def package_time_interval():
    return random.randint(2, 10)


def package_num():
    return random.randint(100, 200)


def process_time():
    return 10  # random.uniform(40, 200)


# 生成货物的process
def generate_package(env, mid):
    package_queue = INPUT_QUEUE_DICT[mid]
    interval = package_time_interval()
    for i in range(package_num()):
        yield env.timeout(interval)
        dest_id = DEST_ID[mid]
        path = (mid, dest_id)
        item = Package(env, None, f'{mid}-{i+1}', path)
        item.next_pipeline = path
        item.time_records.append((path[0], env.now))  # 货物到达机器的时间
        # print(f"package come at {env.now}")
        package_queue.put(item)


if __name__ == '__main__':
    print("start")
    machine_dict = {}
    env = simpy.Environment()

    # 生成输入和输出队列
    for mid in MACHINE_ID:
        INPUT_QUEUE_DICT[mid] = simpy.Store(env)
    for _, did in DEST_ID.items():
        OUTPUT_QUEUE_DICT[did] = simpy.Store(env)

    for mid in MACHINE_ID:
        # 生成货物
        env.process(generate_package(env, mid))
        # 生成机器
        input_queue = INPUT_QUEUE_DICT[mid]
        time = process_time()
        presort_machine = Hospital(env, mid, time, WORKER_NUM, input_queue,
                                   OUTPUT_QUEUE_DICT)
        machine_dict[mid] = presort_machine
        env.process(presort_machine.run())

    env.run()
    print("End.")
