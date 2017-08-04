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


from src.vehicles.items import SmallBag, PackageRecord
import time


BAG_NUM = 15
WAIT_TIME = 7200


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

        self.store = []
        self.counts = 0
        self.store_is_full = self.env.event()

        self.small_bag = []
        self.small_bag_count = 0

        self.resource_set = self._set_machine_resource()

    def _set_machine_resource(self):
        self.equipment_id = self.machine_id[1]
        self.resource_id = self.equipment_resource_dict[self.equipment_id]
        self.resource = self.resource_dict[self.resource_id]['resource']
        self.process_time = self.resource_dict[self.resource_id]['process_time']
        self.last_pipeline = self.pipeline_dict[self.machine_id]
        self.store_max = BAG_NUM
        self.wait_time = WAIT_TIME

    def pack_up_small_bag(self, real_wait_time):
        smallbag = SmallBag(self.env, self.store[0].attr, self.store[:])
        smallbag.item_id = "98" + str(int(time.time() * 1000))[-10:]
        smallbag.set_path(self.equipment_id)
        smallbag.insert_data(
            PackageRecord(
                equipment_id=self.equipment_id,
                package_id=smallbag.item_id,
                time_stamp=self.env.now,
                action="start", ))
        # print(f"{self.env.now}, wait: {real_wait_time}, pack up smallbag: {self.small_bag[-1]}")
        self.small_bag_count += 1
        self.store.clear()
        self.store_is_full = self.env.event()

    def _timer(self):
        start = self.env.now
        yield self.store_is_full | self.env.timeout(self.wait_time)
        end = self.env.now
        real_wait_time = end - start
        self.pack_up_small_bag(real_wait_time)
        yield self.env.timeout(self.process_time)
        self.put_small_bag()

    def put_package(self, item):

        self.store.append(item)

        if len(self.store) == 1:
            self.env.process(self._timer())

        elif len(self.store) == self.store_max:
            self.store_is_full.succeed()

    def put_small_bag(self):
        if self.small_bag:
            for i in range(len(self.small_bag)):
                smallbag = self.small_bag.pop(0)
                smallbag.insert_data(
                    PackageRecord(
                        equipment_id=self.equipment_id,
                        package_id=smallbag.item_id,
                        time_stamp=self.env.now,
                        action="end", ))
                self.pipeline_dict[smallbag.next_pipeline].put(smallbag)

    def run(self):
        while True:
            small = yield self.last_pipeline.get()
            self.put_package(small)
