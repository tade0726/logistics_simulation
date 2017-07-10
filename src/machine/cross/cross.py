# -*- coding: utf-8 -*-

"""
======================================================================================================
                                                     杭州HUB仿真项目

                                    项目启动日期：2017年7月6日
                                    项目启动标识：AIRPORT OF EZHOU'S PROJECT  -- HZ
                                    ===========================================
                                    代码创建日期：2017年7月6日
                                    代码创建工程师：卢健
                                    代码版本：1.0
                                    版本更新日期：2017年7月6日
                                    版本更新工程师：卢健

                                    代码整体功能描述：汇流点机器
                                                      1、二入一出模型， 本次只需要一个入口一个出口；
                                                      2、无延时处理过程；
                                                      3、每个入口无服务受限；
=====================================================================================================
"""


from simpy import PriorityItem


class Cross(object):
    """
    Cross obj:
    sim one machine that have more than one input ports and one out put port.
    input_i wrapped in a dict: input_dic = {'x1_in1': queue, ..., 'x1_ini': queue}.
                  _ _ _ _ _ _ _
                 |             |
     input_1 - ->|             |
         .       |    Cross    |- ->output
     input_i - ->|             |
                 |_ _ _ _ _ _ _|
    """
    def __init__(self, env, id_x, input_dic: dict=None, out_put=None):
        """
        init class self args:
        Args:
            env: A simpy.Environment instance.
            id_x: Cross machine id.
            input_dic: A simpy.PriorityStore which was put from ahead machine.
            out_put: out .

        """
        self.env = env
        self.id_x = id_x
        self.input_dic = input_dic
        self.out_put = out_put
        self.process = self._get_package_queue()

    def _get_package_queue(self):
        """
        """
        if self.input_dic:
            for queue_id, get_package_queue in self.input_dic.items():
                self.env.process(self._get_packages(queue_id, get_package_queue))
        else:
            raise RuntimeError('Please Initial input port Queue for Cross instance First!')

    def _get_packages(self, queue_id, get_package_queue):
        """
        """
        while True:
            packages = yield get_package_queue.get()
            print(f"------->package {packages.item['package_id']}", 'was push to next queue at', self.env.now)
            self.env.process(self._put_packages_into_out_queue(packages))

    def _put_packages_into_out_queue(self, package):
        """
        """
        yield self.out_put.put(PriorityItem(priority=self.env.now, item=package))

