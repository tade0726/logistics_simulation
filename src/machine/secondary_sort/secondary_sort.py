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

        self.package_count = 0

    def secondary_machine(self, package:Package):
        """
        终分拣逻辑
        """
        while True:
            with self.cart.request() as req:
                yield req

                package.start_serve()
                #pipeline功能：指引包裹
                now_loc, next_loc = package.next_pipeline

                yield self.env.timeout(self.process_time)
                package.time_records.append((next_loc, self.env.now))
                package.end_serve()

                self.next_queue[next_loc].put(package)

    def run(self):
        while True:
            package = yield self.last_queue.get()
            self.env.process(self.secondary_machine(package))
