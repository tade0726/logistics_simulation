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
    预分拣机器的仿真
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
        self.process_time = process_time  # 处理时间
        self.worker_num = worker_num  # 资源（工人）数量

        # 入口队列
        self.last_queue = input_queue

        # 出口队列
        self.next_queue = output_queue_dict

        # 人力资源
        self.workers = simpy.Resource(self.env, self.worker_num)

        # check empty
        # self.empty = self.env.event()
        # self.env.process(self.empty_queue())

    # def empty_queue(self):
    #     while True:
    #         if not self.last_queue.items:
    #             self.empty.succeed()
    #             self.empty = self.env.event()
    #         yield self.env.timeout(100)

    def run(self):
        while True:
            # 请求资源（工人）
            with self.workers.request() as req:
                yield req  # 请求到一个资源（工人）

                # 获取一件货物
                package = yield self.last_queue.get()
                package = package.item
                last_position = package.path[0]
                next_position = package.path[1]

                # 处理
                yield self.env.timeout(self.process_time)
                package.path.pop(0)

                # 记录处理完的时间
                package.time_list.append(self.env.now)

                # 放入下一步的传送带
                self.next_queue[next_position].put(
                    simpy.PriorityItem(self.env.now, package))

                # print(
                #     f'Package {package.package_id} go to {next_position} from {last_position} at {self.env.now}')
