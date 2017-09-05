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

from queue import Queue
from src.vehicles.items import SmallBag, SmallPackage
from src.config import SmallCode, LOG
from src.utils import PackageRecordDict


class SmallReload(object):

    def __init__(self,
                 env,
                 equipment_port,
                 pipelines_dict: dict,
                 equipment_process_time_dict: dict,
                 equipment_parameters: dict,
                 data_pipeline: Queue,
                 share_queue_dict: dict,
                 ):
        self.env = env
        self.equipment_port = equipment_port
        self.pipelines_dict = pipelines_dict
        self.equipment_process_time_dict = equipment_process_time_dict
        self.equipment_parameters = equipment_parameters
        self.data_pipeline = data_pipeline
        self.share_queue_dict = share_queue_dict

        self.store = list()
        self.small_bag_count = 0
        # init data
        self._set_machine_resource()
        # wait_time_stamp
        self.wait_times_stamp = None
        # plan pack time
        self._plan_pack_time()

    def _set_machine_resource(self):
        self.process_time = self.equipment_process_time_dict[self.equipment_port]
        self.equipment_name = self.equipment_port.split('_')[0]
        self.parameters =  self.equipment_parameters[self.equipment_name]
        self.store_max = self.parameters['smallbag_wrap_condition']
        self.pack_time_list = [self.parameters[f"smallbag_wrap_time_{i}"] for i in range(1, 7)]
        self.input_pip_line = self.share_queue_dict[self.equipment_port]

    def _plan_pack_time(self):
        """init plan for pack small package"""
        for delay in self.pack_time_list:
            self.env.process(self._time_to_pack(delay))

    def _time_to_pack(self, delay: float):
        """delay certain time and pack"""
        yield self.env.timeout(delay)
        if self.store:
            self.env.process(self.pack_send())

    def _get_small_package(self):
        """pop out package"""
        if len(self.store) <= self.store_max:
            pop_number = len(self.store)
        else:
            pop_number = self.store_max
        store = [self.store.pop(0) for _ in range(pop_number)]
        return store

    def pack_send(self):
        # init small_bag
        store = self._get_small_package()
        small_bag = SmallBag(store, self.data_pipeline)
        small_bag.parcel_id = "98" + next(SmallCode.code_generator)  # "98" + "0000000000" ~ "98" + "9999999999"

        small_bag.insert_data(
            PackageRecordDict(
                equipment_id=self.equipment_port,
                time_stamp=wait_time_stamp,
                action="wait", ), to_small=False)

        small_bag.insert_data(
            PackageRecordDict(
                equipment_id=self.equipment_port,
                time_stamp=self.env.now,
                action="start", ))

        yield self.env.timeout(self.process_time)

        small_bag.insert_data(
            PackageRecordDict(
                equipment_id=self.equipment_port,
                time_stamp=self.env.now,
                action="end", ))

        try:
            small_bag.set_path(self.equipment_port)
            self.pipelines_dict[small_bag.next_pipeline].put(small_bag)
        except Exception as exc:
            # 收集错错误的小件包裹
            self.pipelines_dict["small_reload_error"].put(small_bag)
            msg = f"error: {exc}, package: {small_bag}, equipment_id: {self.equipment_port}"
            LOG.logger_font.error(msg)
            LOG.logger_font.exception(exc)

        self.small_bag_count += 1

    def put_package(self, small: SmallPackage):
        """put package into store"""
        self.store.append(small)

        if len(self.store) == 1:
            self.wait_times_stamp = self.env.now

        elif len(self.store) >= self.store_max:
            self.env.process(self.pack_send())

    def run(self):
        while True:
            small = yield self.input_pip_line.get()
            self.put_package(small)
