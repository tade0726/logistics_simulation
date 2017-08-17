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
from src.config import LOG


class SecondarySort(object):

    def __init__(self,
                 env: simpy.Environment(),
                 machine_id: tuple,
                 pipelines_dict: dict,
                 ):

        self.env = env
        self.machine_id = machine_id
        self.pipelines_dict = pipelines_dict

        # add machine switch
        self.machine_switch = self.env.event()
        self.machine_switch.succeed()

        self._set_machine()

    def _set_machine(self):
        """
        """
        self.equipment_id = self.machine_id[1]  # pipeline id last value, for other machines
        self.input_pip_line = self.pipelines_dict[self.machine_id]

    def set_machine_open(self):
        """设置为开机"""
        self.machine_switch.succeed()

    def set_machine_close(self):
        """设置为关机"""
        self.machine_switch = self.env.event()

    def run(self):
        while True:
            # 开关机的事件控制
            yield self.machine_switch

            package = yield self.input_pip_line.get()
            try:
                self.pipelines_dict[package.next_pipeline].put(package)
            except Exception as exc:
                self.pipelines_dict['error'].put(package)
                msg = f"error: {exc}, package: {package}, equipment_id: {self.equipment_id}"
                LOG.logger_font.error(msg)
                LOG.logger_font.exception(exc)
