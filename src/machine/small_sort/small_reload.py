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

from src.vehicles.items import SmallBag, SmallPackage
from src.config import SmallCode, LOG
from src.utils import PackageRecordDict


class SmallReload(object):

    def __init__(self,
                 env,
                 machine_id,
                 pipelines_dict: dict,
                 equipment_process_time_dict: dict,
                 pack_time_list: list,
                 equipment_parameters: dict,
                 ):
        self.env = env
        self.machine_id = machine_id
        self.pipelines_dict = pipelines_dict
        self.equipment_process_time_dict = equipment_process_time_dict
        self.pack_time_list = pack_time_list
        self.equipment_parameters=equipment_parameters

        self.store = list()
        self.small_bag_count = 0
        # event for control
        self.store_is_full = self.env.event()
        # pack small package events
        self.pack_time_is_up = self.env.event()
        # init data
        self._set_machine_resource()
        # plan pack time
        self._plan_pack_time()

    def _set_machine_resource(self):
        self.equipment_id = self.machine_id[1]
        self.process_time = self.equipment_process_time_dict[self.equipment_id]
        self.last_pipeline = self.pipelines_dict[self.machine_id]
        self.equipment_name = self.machine_id.split('_')[0]  # r1, ect
        self.store_max = self.equipment_parameters[self.equipment_name]["smallbag_wrap_condition"]

    def _set_pack_event(self, delay: float):
        """setting pack event"""
        yield self.env.timeout(delay)
        self.pack_time_is_up.succeed()
        self.pack_time_is_up = self.env.event()

    def _plan_pack_time(self):
        """init plan for pack small package"""
        for delay in self.pack_time_list:
            self.env.process(self._set_pack_event(delay))

    def _get_small_package(self):
        """pop out package"""
        if len(self.store) <= self.store_max:
            pop_number = len(self.store)
        else:
            pop_number = self.store_max
        store = [self.store.pop(0) for _ in range(pop_number)]
        return store

    def pack_send(self, wait_time_stamp: float):
        # init small_bag
        store = self._get_small_package()
        small_bag = SmallBag(store)
        small_bag.parcel_id = "98" + next(SmallCode.code_generator)  # "98" + "0000000000" ~ "98" + "9999999999"

        small_bag.insert_data(
            PackageRecordDict(
                equipment_id=self.equipment_id,
                time_stamp=wait_time_stamp,
                action="wait", ), to_small=False)

        small_bag.insert_data(
            PackageRecordDict(
                equipment_id=self.equipment_id,
                time_stamp=self.env.now,
                action="start", ))

        yield self.env.timeout(self.process_time)

        small_bag.insert_data(
            PackageRecordDict(
                equipment_id=self.equipment_id,
                time_stamp=self.env.now,
                action="end", ))

        try:
            small_bag.set_path(self.equipment_id)
            self.pipelines_dict[small_bag.next_pipeline].put(small_bag)
        except Exception as exc:
            # 收集错错误的小件包裹
            self.pipelines_dict["small_reload_error"].put(small_bag)
            msg = f"error: {exc}, package: {small_bag}, equipment_id: {self.equipment_id}"
            LOG.logger_font.error(msg)
            LOG.logger_font.exception(exc)

        self.small_bag_count += 1

    def _timer(self):
        """decide when to pack a small bag"""
        wait_time_stamp = self.env.now
        yield self.store_is_full | self.pack_time_is_up
        self.env.process(self.pack_send(wait_time_stamp))

    def put_package(self, small: SmallPackage):
        """put package into store"""
        self.store.append(small)

        if len(self.store) == 1:
            self.env.process(self._timer())

        elif len(self.store) == self.store_max:
            self.store_is_full.succeed()
            self.store_is_full = self.env.event()

    def run(self):
        while True:
            small = yield self.last_pipeline.get()
            self.put_package(small)
