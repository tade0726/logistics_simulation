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
from src.machine.secondary_sort import SecondarySort
from src.vehicles.items import Package


RANDOM_SEED = 42
CART_NUM = 300
MACHINE_ID = ["i2-1", "i2-2", "i2-3"]
DEST_NUM = 3
DEST_ID = {}
ALL_PACKAGES = {}
INPUT_QUEUE_DICT = {}
OUTPUT_QUEUE_DICT = {}


# 生成单个入口包裹到达的时间间隔
def package_time_interval():
    return random.uniform(40, 60)


# 生成单个入口包裹队列的长度
def package_num():
    return random.randint(5, 10)


# 生成出口编号
def generate_dest_id():
    dest_list = []
    for mid in MACHINE_ID:
        DEST_ID[mid] = []
        for i in range(DEST_NUM):
            DEST_ID[mid].append(mid.replace("i", "c")[0:3] + str(i + 1))
        dest_list += DEST_ID[mid]
    return list(set(dest_list))


class PackageSecondary(object):
    """
    测试用包裹类
    """

    def __init__(self, package_id, path, generate_time, env):
        self.package_id = package_id
        self.path = path[:]
        self.plan_path = path[:]
        self.time_list = [generate_time]
        self.time_records = []
        self.env = env

    def ret_pop_mark(self):
        """返回下一个pipeline id: (now_loc, next_loc)， 删去第一个节点，记录当前的时间点"""

        if len(self.path) >= 2:
            now_loc, next_loc = self.path[0: 2]
        # 当 package 去到 reload（终分拣）， 终分拣的队列 id 只有一个值
        elif len(self.path) == 1:
            now_loc, next_loc = self.path[-1], None
        else:
            raise ValueError('The path have been empty!')
        # remove the now_loc
        pop_loc = self.path.pop(0)
        self.time_records.append((pop_loc, self.env.now))
        return now_loc, next_loc


# 生成所有的输入包裹
def generate_package():
    for mid in MACHINE_ID:
        interval = package_time_interval()
        dest_id = random.choice(DEST_ID[mid])
        path = [mid, dest_id]
        ALL_PACKAGES[mid] = []
        for i in range(package_num()):
            ALL_PACKAGES[mid].append(
                PackageSecondary(f'package{mid}-{i+1}', path, interval * i, simpy.Environment()))


# 生成输入队列
def generate_queue(env, machine_id):
    package_queue = simpy.PriorityStore(env)
    for i in range(len(ALL_PACKAGES[machine_id])):
        item = ALL_PACKAGES[machine_id].pop(0)
        package_queue.put(
            simpy.PriorityItem(priority=item.time_list[0], item=item))
    INPUT_QUEUE_DICT[machine_id] = package_queue


def secondary_sim():
    dest_id_list = generate_dest_id()
    generate_package()
    machine_dict = {}
    env = simpy.Environment()
    for did in dest_id_list:
        OUTPUT_QUEUE_DICT[did] = simpy.PriorityStore(env)
    for mid in MACHINE_ID:
        generate_queue(env, mid)
        input_queue = INPUT_QUEUE_DICT[mid]
        secondary_machine = SecondarySort(env, input_queue, mid, CART_NUM,
                                  OUTPUT_QUEUE_DICT)
        machine_dict[mid] = secondary_machine
        env.process(secondary_machine.secondary_machine())
    env.run()


if __name__ == '__main__':
    print("start")
    secondary_sim()
    print("End")