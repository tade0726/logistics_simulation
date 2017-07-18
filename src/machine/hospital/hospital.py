# -*- coding: utf-8 -*-

"""
==================================================================================================================================================
                                                     杭州HUB仿真项目

                                    项目启动日期：2017年7月6日
                                    项目启动标识：AIRPORT OF EZHOU'S PROJECT  -- HZ
                                    ===========================================
                                    代码创建日期：2017年7月13日
                                    代码创建工程师：谈和
                                    代码版本：1.0
                                    版本更新日期：2017年7月13日
                                    版本更新工程师：谈和

                                    代码整体功能描述：医院区处理模块，处理逻辑；
                                                    处理逻辑：从前一个队列（last_queue)取出货物，
                                                    加上处理时间，
                                                    然后放置到下一个队列(next_queue)；



==================================================================================================================================================
"""

import simpy
from src.vehicles.items import Package


class Hospital(object):
    """
    医院区机器的仿真
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

        # 检查队列是否为空， TODO 为了跑测试程序，将第二行注释，正式程序需去掉注释
        self.empty = self.env.event()
        # self.env.process(self.empty_queue())

        # 等待队列包裹数
        self.package_counts = 0

    def empty_queue(self):
        """
        实时判断，如果连接此机器的队列为空，则触发self.empty事件
        """
        while True:
            if not self.package_counts:
                self.empty.succeed()
                self.empty = self.env.event()
            yield self.env.timeout(100)

    def processing(self, package: Package):
        # 请求资源（工人)
        with self.workers.request() as req:
            yield req
            # 获取一件货物
            # 获取当前位置、下一步位置，增加时间记录
            now_loc, next_loc = package.next_pipeline
            # 增加处理时间
            yield self.env.timeout(self.process_time)
            # 放入下一步的传送带
            self.next_queue[next_loc].put(package)
            # 记录时间
            package.time_records.append((next_loc, self.env.now))
            # 计数等待处理的包裹
            self.package_counts -= 1
            print(
                f'Package {package.item_id} arrive in {package.time_records[0][0]} at {package.time_records[0][1]}' +
                f', processed at {package.time_records[1][1]}' +
                f', wait {package.time_records[1][1] - package.time_records[0][1]}' +
                f', next to {package.path[1]}'
                f', {self.package_counts} packages waiting at {package.time_records[0][0]}.'
            )

    def run(self):
        while True:
            package = yield self.last_queue.get()
            # 计数等待处理的包裹
            self.package_counts += 1
            self.env.process(self.processing(package))
