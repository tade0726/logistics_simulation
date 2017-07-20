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
from src.vehicles.items import Package
from src.utils import PackageRecord


class SecondarySort(object):

    def __init__(self,
                 env: simpy.Environment(),
                 machine_id: tuple,
                 pipelines_dict: dict,):

        self.env = env
        self.machine_id = machine_id
        self.equipment_id = machine_id[0]
        self.pipelines_dict = pipelines_dict
        self.last_pipeline = pipelines_dict[machine_id]

    def run(self):
        while True:
            package = yield self.last_pipeline.get()
            next_pipeline = package.next_pipeline
            self.pipelines_dict[next_pipeline].put(package)
