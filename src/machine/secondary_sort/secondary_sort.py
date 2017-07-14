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


class SecondarySort(object):
    def __init__(self, env: simpy.Environment(),
            queue: simpy.PriorityStore,
            machine_id: str, cart_num: int, output_queue_dict):
        self.env = env
        self.machine_id = machine_id
        self.queue = queue
        # 资源池小车数量
        self.cart_num = cart_num
        # todo @lanyi：口对应设备，查code
        self.cart = simpy.Resource(self.env, self.cart_num)

        # check empty
        self.empty = self.env.event()
        # self.env.process(self.empty_queue())

        self.tmp_queue = simpy.Store(self.env)

    # def empty_queue(self):
    #     """
    #     达到特定条件的时候，证明机器为空
    #     """
    #     while True:
    #         if not self.queue.items:
    #             self.empty.succeed()
    #             self.empty = self.env.event()
    #         yield self.env.timeout(100)

    def secondary_machine(self):
        """
        终分拣逻辑
        """
        while True:
            with self.cart.request() as req:
                package = yield self.queue.get()
                package = package.item
                #pipeline功能：指引包裹
                pipeline_id = package.ret_pop_mark()
                # todo @lanyi: 预留装车位置

                yield self.tmp_queue.put(package)

                # todo @lanyi: 最终代码没有以下代码
                if package:
                    print(f"{package.package_id} go to {package.plan_path[0]} at {package.time_list[0]}")
