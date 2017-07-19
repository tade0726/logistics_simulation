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
from src.vehicles.items import Package


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
        item = Package(env, None, f'{mid}-{i+1}', path)
        item.next_pipeline = path
        item.time_records.append((path[0], env.now))
        package_queue.put(item)


class SecondarySort(object):
    """
    预分拣机器的仿真
    """
    def __init__(self,
                 env: simpy.Environment,
                 machine_id: str,
                 process_time: float,
                 cart_num: int,
                 input_queue,
                 output_queue_dict
                 ):
        """

        """
        self.env = env
        self.machine_id = machine_id
        self.process_time = process_time  # 处理时间
        self.cart_num = cart_num  # 资源（工人）数量

        # 入口队列
        self.last_queue = input_queue

        # 出口队列
        self.next_queue = output_queue_dict

        # 人力资源
        self.carts = simpy.Resource(self.env, self.cart_num)

        # 检查队列是否为空， TODO 为了跑测试程序，将第二行注释，正式程序需去掉注释
        self.empty = self.env.event()
        # self.env.process(self.empty_queue())

        # 等待队列包裹数
        self.package_counts = 0

    def secondary_machine(self, package: Package):
        with self.carts.request() as req:
            yield req
            start_time = package.start_serve()
            now_loc, next_loc = package.next_pipeline
            yield self.env.timeout(self.process_time)
            self.next_queue[next_loc].put(package)
            package.time_records.append((next_loc, self.env.now))
            end_time = package.end_serve()
            print(
                f'Package {package.item_id} arrive in {now_loc} at '
                f'{package.package_record["start_serve"]} process {self.process_time} '
                f'going to {next_loc} end {package.package_record["end_serve"]}'
            )

    def run(self):
        while True:
            package = yield self.last_queue.get()
            self.package_counts += 1
            self.env.process(self.secondary_machine(package))


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
        cou = 1
        count = str(cou)
        env.process(generate_package(env, mid))
        input_queue = INPUT_QUEUE_DICT[mid]
        time = 10
        secondary_sort_machine = SecondarySort(env, count, time, CART_NUM, input_queue,
                                  OUTPUT_QUEUE_DICT)
        machine_dict[mid] = secondary_sort_machine
        env.process(secondary_sort_machine.run())
        cou += 1

    env.run()
    print("End.")