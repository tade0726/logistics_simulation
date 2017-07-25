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
from src.vehicles import Package
from src.utils import PackageRecord


class SecondarySort(object):

    def __init__(self,
                 env: simpy.Environment(),
                 machine_id: tuple,
                 pipelines_dict: dict,
                 equipment_process_time:dict,
                 ):

        self.env = env
        self.machine_id = machine_id
        self.pipelines_dict = pipelines_dict
        self.equipment_process_time = equipment_process_time
        self._set_machine_resource()

    def _set_machine_resource(self):
        """
        """
        self.equipment_id = self.machine_id   # pipeline id last value, for other machines
        self.process_time = self.equipment_process_time[self.equipment_id]
        self.input_pip_line = self.pipelines_dict[self.machine_id]

    def process_package(self, item: Package):
        # package start for process
        item.insert_data(
            PackageRecord(
                equipment_id=self.equipment_id,
                package_id=item.item_id,
                time_stamp=self.env.now,
                action="start", ))

        yield self.env.timeout(self.process_time)

        # package end for process
        item.insert_data(
            PackageRecord(
                equipment_id=self.equipment_id,
                package_id=item.item_id,
                time_stamp=self.env.now,
                action="end", ))

        next_pipeline = item.next_pipeline
        self.pipelines_dict[next_pipeline].put(item)

    def run(self):
        while True:
            package = yield self.input_pip_line.get()
            self.env.process(self.process_package(item=package))
