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
from src.machine import BaseMachine


class SecondarySort(BaseMachine):

    def __init__(self,
                 env: simpy.Environment(),
                 machine_id: tuple,
                 pipelines_dict: dict,
                 ):

        super(SecondarySort, self).__init__(env)
        self.machine_id = machine_id
        self.pipelines_dict = pipelines_dict

        self._set_machine()

    def _set_machine(self):
        """
        """
        self.equipment_id = self.machine_id[1]  # pipeline id last value, for other machines
        self.input_pip_line = self.pipelines_dict[self.machine_id]

    def run(self):
        while True:
            try:
                package = yield self.input_pip_line.get()
            except simpy.Interrupt:
                self.close = True
                LOG.logger_font.debug(f"sim time: {self.env.now} - equipment: {self.equipment_id} - close 1800s")
                yield self.env.timeout(1800)
                break

            try:
                self.pipelines_dict[package.next_pipeline].put(package)
            except Exception as exc:
                self.pipelines_dict['error'].put(package)
                msg = f"error: {exc}, package: {package}, equipment_id: {self.equipment_id}"
                LOG.logger_font.error(msg)
                LOG.logger_font.exception(exc)
