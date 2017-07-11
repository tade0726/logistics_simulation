# -*- coding: utf-8 -*-

"""
==================================================================================================================================================
                                                     杭州HUB仿真项目

                                    项目启动日期：2017年7月6日
                                    项目启动标识：AIRPORT OF EZHOU'S PROJECT  -- HZ
                                    ===========================================
                                    代码创建日期：2017年7月6日
                                    代码创建工程师：谈和，元方
                                    代码版本：1.0
                                    版本更新日期：2017年7月11日
                                    版本更新工程师：元方

                                    代码整体功能描述：预分拣模块，
                                                      1、完成预分拣模块的货物处理逻辑；



==================================================================================================================================================
"""


import simpy


class Presort(object):
    """
    Simulate pre-sort
    """
    def __init__(self,
                 env: simpy.Environment,
                 machine_id: str,
                 process_time: float,
                 worker_num: int,
                 input_queue,
                 output_queue_dict
                 ):
        """

        """
        self.env = env
        self.machine_id = machine_id
        self.process_time = process_time  # process time
        self.worker_num = worker_num  # resource capacity
        self.last_queue = input_queue

        # next queue
        self.next_queue = output_queue_dict

        # resources
        self.workers = simpy.Resource(self.env, self.worker_num)

        # check empty
        self.empty = self.env.event()
        self.env.process(self.empty)

    def empty_queue(self):
        while True:
            if not self.last_queue.items:
                self.empty.succeed()
                self.empty = self.env.event()
            yield self.env.timeout(100)

    def run(self):
        while True:
            # request a worker to process this package
            with self.workers.request() as req:
                yield req  # access to a worker

                # get one package
                package = yield self.last_queue.get()
                package = package.item
                last_position = package.path[0]
                next_position = package.path[1]

                # processing
                yield self.env.timeout(self.process_time)
                package.path.pop(0)

                # record time
                package.time_list.append(self.env.now)

                # put the package
                self.next_queue[next_position].put(simpy.PriorityItem(self.env.now, package))
