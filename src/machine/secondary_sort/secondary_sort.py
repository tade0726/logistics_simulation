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
from collections import defaultdict


class SecondarySort(object):

    def __init__(self,
                 env: simpy.Environment(),
                 machine_id: tuple,
                 pipelines_dict: dict,
                 resource_dict: defaultdict,
                 equipment_resource_dict: dict,
                 ):

        self.env = env
        self.machine_id = machine_id
        self.pipelines_dict = pipelines_dict
        self.resource_dict = resource_dict
        self.equipment_resource_dict = equipment_resource_dict
        self._set_machine_resource()

    def _set_machine_resource(self):
        """
        """
        if self.equipment_resource_dict:
            self.equipment_id = self.machine_id   # pipeline id last value, for other machines
            self.resource_id = self.equipment_resource_dict[self.equipment_id]
            self.resource = self.resource_dict[self.resource_id]['resource']
            self.process_time = self.resource_dict[self.resource_id]['process_time']
            self.input_pip_line = self.pipelines_dict[self.machine_id]

    # todo:
    def process_package(self, item: Package):
        yield self.env.timeout(self.process_time)

    def run(self):
        while True:
            package = yield self.input_pip_line.get()
            next_pipeline = package.next_pipeline

            # package start for process
            package.insert_data(
                PackageRecord(
                    equipment_id=self.equipment_id,
                    package_id=package.item_id,
                    time_stamp=self.env.now,
                    action="start", ))

            # package end for process
            package.insert_data(
                PackageRecord(
                    equipment_id=self.equipment_id,
                    package_id=package.item_id,
                    time_stamp=self.env.now,
                    action="end", ))

            self.pipelines_dict[next_pipeline].put(package)

