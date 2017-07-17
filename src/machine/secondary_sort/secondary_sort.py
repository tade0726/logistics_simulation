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
from src.vehicles.items import Package


class SecondarySort(object):
    def __init__(self,
                 env: simpy.Environment(),
                 machine_id: str,
                 process_time: float,
                 cart_num: int,
                 input_queue: simpy.PriorityStore,
                 output_queue):
        self.env = env
        self.machine_id = machine_id
        self.process_time = process_time
        self.cart_num = cart_num

        self.last_queue = input_queue

        self.next_queue = output_queue

        self.cart = simpy.Resource(self.env, self.cart_num)

        # check empty
        # self.empty = self.env.event()
        # self.env.process(self.empty_queue())

        self.package_count = 0

    # def empty_queue(self):
    #     """
    #     达到特定条件的时候，证明机器为空
    #     """
    #     while True:
    #         if not self.queue.items:
    #             self.empty.succeed()
    #             self.empty = self.env.event()
    #         yield self.env.timeout(100)

    def secondary_machine(self, package:Package):
        """
        终分拣逻辑
        """
        while True:
            with self.cart.request() as req:
                yield req

                #pipeline功能：指引包裹
                pipeline_id = package.ret_pop_mark()

                yield self.env.timeout(self.process_time)

                self.next_queue[pipeline_id].put(package)

                self.package_count -= 1

                print(f'{pipeline_id}')

    def run(self):
        while True:
            package = yield self.last_queue.get()
            self.package_count += 1
            self.env.process(self.secondary_machine(package))