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
                                    版本更新日期：2017年7月12日
                                    版本更新工程师：元方

                                    代码整体功能描述：预分拣机器测试单元


=====================================================================================================
"""

import simpy
import random

# from src.machine.presort import Presort


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
    return random.uniform(40, 60)


# 生成单个入口包裹队列的长度
def package_num():
    return random.randint(5, 10)


# 生成一个入口到一个出口的处理时间
def process_time():
    return random.uniform(40, 200)


# 生成出口编号
def generate_dest_id():
    dest_list = []
    for mid in MACHINE_ID:
        DEST_ID[mid] = []
        for i in range(DEST_NUM):
            DEST_ID[mid].append(mid.replace("m", "i")[0:3] + str(i + 1))
        dest_list += DEST_ID[mid]
    return list(set(dest_list))


class PackagePresort(object):
    """
    测试用包裹类
    """

    def __init__(self, package_id, path, generate_time):
        self.package_id = package_id
        self.path = path[:]
        self.plan_path = path[:]
        self.time_list = [generate_time]


# 生成所有的输入包裹
def generate_package():
    for mid in MACHINE_ID:
        interval = package_time_interval()
        dest_id = random.choice(DEST_ID[mid])
        path = [mid, dest_id]
        ALL_PACKAGES[mid] = []
        for i in range(package_num()):
            ALL_PACKAGES[mid].append(
                PackagePresort(f'{mid}-{i+1}', path, interval * i))


# 生成输入队列
def generate_queue():
    pass


if __name__ == '__main__':
    print("start")
    dest_id_list = generate_dest_id()
    generate_package()
    machine_dict = {}
    env = simpy.Environment()
    for did in dest_id_list:
        OUTPUT_QUEUE_DICT[did] = simpy.PriorityStore(env)

    env.run()
    for machine_id in MACHINE_ID:
        for item in ALL_PACKAGES[machine_id]:
            print(
                f'Package {item.package_id} go to {machine_id} at {item.time_list[0]}')
    print("End")
