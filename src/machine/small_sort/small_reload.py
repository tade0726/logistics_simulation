# -*- coding: utf-8 -*-

"""
==================================================================================================================================================
                                                     杭州HUB仿真项目

                                    项目启动日期：2017年7月6日
                                    项目启动标识：AIRPORT OF EZHOU'S PROJECT  -- HZ
                                    ===========================================
                                    代码创建日期：2017年7月日
                                    代码创建工程师：元方
                                    代码版本：1.0
                                    版本更新日期：2017年7月日
                                    版本更新工程师：

                                    代码整体功能描述：小件打包模块



==================================================================================================================================================
"""


from src.vehicles.items import SmallPackage, SmallBag, PackageRecord
import time


BAG_NUM = 15

class SmallReload(object):

    def __init__(self,
                 env,
                 machine_id,
                 pipeline_dict=None,
                 resource_dict=None,
                 equipment_resource_dict=None):
        self.env = env
        self.machine_id = machine_id
        self.pipeline_dict = pipeline_dict
        self.resource_dict = resource_dict
        self.equipment_resource_dict = equipment_resource_dict
        self.resource_set = self._set_machine_resource()
        self.small_list = []
        self.timer = 0

    def _set_machine_resource(self):
        self.equipment_id = self.machine_id[1]
        self.resource_id = self.equipment_resource_dict[self.equipment_id]
        self.resource = self.resource_dict[self.resource_id]['resource']
        self.process_time = self.resource_dict[self.resource_id]['process_time']
        self.last_pipeline = self.pipeline_dict[self.machine_id]
        self.bag_num = BAG_NUM

    def length(self):
        return len(self.small_list)

    def processing(self):
        if self.length == self.bag_num or self.env.now - self.timer > 7200:
            smallbag = SmallBag(self.env, self.small_list[0].attr,
                                self.small_list)
            smallbag.item_id = "98" + str(int(time.time()*1000))[-10:]
            smallbag.set_path(self.equipment_id)
            output_pipeline = smallbag.next_pipeline
            # 记录机器开始处理货物信息
            smallbag.insert_data(
                PackageRecord(
                    equipment_id=self.equipment_id,
                    package_id=smallbag.item_id,
                    time_stamp=self.env.now,
                    action="start", ))
            # 增加处理时间
            yield self.env.timeout(self.process_time)
            # 记录机器结束处理货物信息
            smallbag.insert_data(
                PackageRecord(
                    equipment_id=self.equipment_id,
                    package_id=smallbag.item_id,
                    time_stamp=self.env.now,
                    action="end", ))
            # 放入下一步的传送带
            self.pipeline_dict[output_pipeline].put(smallbag)
            self.small_list = []

    def run(self):
        while True:
            small = yield self.last_pipeline.get()
            self.small_list.append(small)
            if len(self.small_list) == 1:
                self.timer = self.env.now
            self.env.process(self.processing())
