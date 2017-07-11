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

                                    代码整体功能描述：程序的启动文件，
                                                      1、所有机器参数、全局参数初始化；
                                                      2、模拟终分拣及捷径线队列；



==================================================================================================================================================
"""


import simpy


class SecondarySort:
    def __init__(self, env, machine_id, queue, logger):
        self.env = env
        self.machine_id = machine_id
        self.queue = queue

        self.log_error = logger(log_name=f"error_{self.machine_id}")

        self.wait_queue = simpy.PriorityStore(self.env)

    def machine(self, time):
        while True:
            yield self.env.timeout(time)

    def shortcut(self, time):
        while True:
            #todo @lanyi: deal with pipeline
            pass

    def run(self):
        while True:
            package = yield self.wait_queue.get()
            package = package.item
            destination = package.attr['dest_code']
            process_time = package.attr['time']
            self.shortcut(process_time)
            #todo @lanyi will be replaced with a function
            if destination in ['c1']:
                #todo @lanyi shortcut function
                pass
            self.env.process(self.machine(process_time))
