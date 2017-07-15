# -*- coding: utf-8 -*-

"""
======================================================================================================
                                                     杭州HUB仿真项目

                                    项目启动日期：2017年7月6日
                                    项目启动标识：AIRPORT OF EZHOU'S PROJECT  -- HZ
                                    ===========================================
                                    代码创建日期：2017年7月12日
                                    代码创建工程师：元方
                                    代码版本：1.0
                                    版本更新日期：2017年7月13日
                                    版本更新工程师：元方

                                    代码整体功能描述：预分拣机器测试单元


=====================================================================================================
"""

import simpy
import random
from src.machine.presort import Presort
from src.vehicles.items import Package, Pipeline


RANDOM_SEED = 42
WORKER_NUM = 2
MACHINE_ID = ["m1-1", "m1-2", "m1-3", "m1-4"]
DEST_NUM = 3
DEST_ID = {}
ALL_PACKAGES = {}
INPUT_QUEUE_DICT = {}
OUTPUT_QUEUE_DICT = {}
random.seed(RANDOM_SEED)


# 生成单个入口包裹到达的时间间隔
def package_time_interval():
    # return random.uniform(40, 60)
    return random.randint(2, 10)

# 生成单个入口包裹队列的长度
def package_num():
    return random.randint(100, 200)

# 生成一个入口到一个出口的处理时间
def process_time():
    # return random.uniform(40, 200)
    return 10 #random.randint(10, 30)

# 生成出口编号
def generate_dest_id():
    dest_list = []
    for mid in MACHINE_ID:
        DEST_ID[mid] = []
        for i in range(DEST_NUM):
            DEST_ID[mid].append(mid.replace("m", "i")[0:3] + str(i + 1))
        dest_list += DEST_ID[mid]
    return list(set(dest_list))

# 生成货物的process
def generate_package(env, mid):
    package_queue = INPUT_QUEUE_DICT[mid]
    interval = package_time_interval()
    for i in range(package_num()):
        yield env.timeout(interval)
        dest_id = random.choice(DEST_ID[mid])
        path = (mid, dest_id)
        item = Package(env, None, f'{mid}-{i+1}', path)
        item.time_records.append((path[0], env.now)) # 货物到达机器的时间
        # print(f"package come at {env.now}")
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

    for mid in MACHINE_ID:
        # 生成货物
        env.process(generate_package(env, mid))
        # 生成机器
        input_queue = INPUT_QUEUE_DICT[mid]
        time = process_time()
        presort_machine = Presort(env, mid, time, WORKER_NUM, input_queue,
                                  OUTPUT_QUEUE_DICT)
        machine_dict[mid] = presort_machine
        env.process(presort_machine.run())

    env.run()
    print("End.")
