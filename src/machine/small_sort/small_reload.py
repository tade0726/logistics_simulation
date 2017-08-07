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


from src.vehicles.items import SmallBag, PackageRecord, SmallPackage
from src.config import Small_code, LOG


BAG_NUM = 15
WAIT_TIME = 7200


class SmallReload(object):

    def __init__(self,
                 env,
                 machine_id,
                 pipelines_dict=None,
                 resource_dict=None,
                 equipment_resource_dict=None):
        self.env = env
        self.machine_id = machine_id
        self.pipelines_dict = pipelines_dict
        self.resource_dict = resource_dict
        self.equipment_resource_dict = equipment_resource_dict

        self.store = list()
        self.counts = 0
        self.small_bag_count = 0
        self.store_is_full = self.env.event()

        self._set_machine_resource()

    def _set_machine_resource(self):
        self.equipment_id = self.machine_id[1]
        self.resource_id = self.equipment_resource_dict[self.equipment_id]
        self.resource = self.resource_dict[self.resource_id]['resource']
        self.process_time = self.resource_dict[self.resource_id]['process_time']
        self.last_pipeline = self.pipelines_dict[self.machine_id]
        self.store_max = BAG_NUM
        self.wait_time = WAIT_TIME

    def pack_send(self, wait_time_stamp: float):

        # init small_bag
        small_bag = SmallBag(self.env, self.store[0].attr, self.store[:])
        small_bag.item_id = "98" + next(Small_code.code_generator)  # "98" + "0000000000" ~ "98" + "9999999999"

        self.small_bag_count += 1
        self.store.clear()
        self.store_is_full = self.env.event()

        small_bag.insert_data(
            PackageRecord(
                equipment_id=self.equipment_id,
                package_id=small_bag.item_id,
                time_stamp=wait_time_stamp,
                action="wait", ), to_small=False)

        small_bag.insert_data(
            PackageRecord(
                equipment_id=self.equipment_id,
                package_id=small_bag.item_id,
                time_stamp=self.env.now,
                action="start", ))

        yield self.env.timeout(self.process_time)

        small_bag.insert_data(
            PackageRecord(
                equipment_id=self.equipment_id,
                package_id=small_bag.item_id,
                time_stamp=self.env.now,
                action="end", ))

        try:
            small_bag.set_path(self.equipment_id)
            self.pipelines_dict[small_bag.next_pipeline].put(small_bag)
        except Exception as exc:
            msg = f"error: {exc}, package: {small_bag}, equipment_id: {self.equipment_id}"
            LOG.logger_font.error(msg)
            LOG.logger_font.exception(exc)
            # 收集错错误的小件包裹
            self.pipelines_dict["small_reload_error"].put(small_bag)

    def _timer(self):
        wait_time_stamp = self.env.now
        yield self.store_is_full | self.env.timeout(self.wait_time)
        self.pack_send(wait_time_stamp)

    def put_package(self, small: SmallPackage):

        small.insert_data(
            PackageRecord(
                equipment_id=self.equipment_id,
                package_id=small.item_id,
                time_stamp=self.env.now,
                action="start", ))

        self.store.append(small)

        if len(self.store) == 1:
            self.env.process(self._timer())

        elif len(self.store) == self.store_max:
            self.store_is_full.succeed()

    def run(self):
        while True:
            small = yield self.last_pipeline.get()
            self.put_package(small)
