# -*- coding: utf-8 -*-

"""
作者：Ted
日期：2017-07-13
说明：

包裹 class
货物 class
Uld class

"""
import simpy
import pandas as pd
import numpy as np
from collections import defaultdict
import random
from multiprocessing import Queue


from src.utils import \
    (PackageRecord, PipelineRecord, TruckRecord, PathGenerator, TruckRecordDict, PackageRecordDict, PipelineRecordDict)

from src.utils import \
    (PathRecordDict, PathRecord)

from src.config import LOG

__all__ = ["Parcel", "Package", "Truck", "Uld", "SmallBag", "SmallPackage", "Pipeline", "PipelineRes", "BasePipeline",
           "PipelineReplace",]


path_g = PathGenerator()


class Package:
    """包裹"""
    def __init__(self,
                 attr: pd.Series,
                 data_pipeline: Queue):

        # 包裹的所有信息都在 attr
        self.attr = attr
        # id
        self._parcel_id = self.attr["parcel_id"]
        self.small_id = self.attr.get("small_id", self._parcel_id)
        # data store
        self.machine_data = list()
        self.pipeline_data = list()
        self.path_request_data = list()

        # 数据队列，在仿真的过程中同时被消费
        self.data_pipeline = data_pipeline

        # path_generator
        self.path_g = path_g
        # paths
        self.planned_path = None
        self.path = None
        # next pipeline_id
        self.next_pipeline = None

        self.ident_des_zno = self.attr["ident_des_zno"]
        self.dest_type = self.attr["dest_type"]
        # parcel_type: {'nc', 'small', 'parcel'}
        self.parcel_type = self.attr["parcel_type"]
        self.sorter_type = "small_sort" if self.parcel_type == "small" else "reload"

    @property
    def parcel_id(self):
        return self._parcel_id

    @parcel_id.setter
    def parcel_id(self, value: str):
        self._parcel_id = value

    # use in unload machine
    def set_path(self, package_start):
        ret_path = self.path_g.path_generator(package_start, self.ident_des_zno, self.sorter_type, self.dest_type)
        self.planned_path = tuple(ret_path)
        self.path = list(self.planned_path)
        self.next_pipeline = self.planned_path[:2]

        # collection path data
        data = PathRecordDict(
            start_node=package_start,
            ret_path=':'.join(ret_path),
        )
        # add data
        self.insert_data(data)

    def insert_data(self, data: dict):

        if isinstance(data, PackageRecordDict):
            record = PackageRecord(
                parcel_id=self.parcel_id,
                small_id=self.small_id,
                parcel_type=self.parcel_type,
                **data,
            )

            self.machine_data.append(record)
            self.data_pipeline.put(record)

            LOG.logger_font.debug(msg=f"Package: {record.small_id} , action: {record.action}"
                                      f", equipment: {record.equipment_id}, timestamp: {record.time_stamp}")


        elif isinstance(data, PipelineRecordDict):
            record = PipelineRecord(
                parcel_id=self.parcel_id,
                small_id=self.small_id,
                parcel_type=self.parcel_type,
                **data,
            )

            self.pipeline_data.append(record)
            self.data_pipeline.put(record)

            LOG.logger_font.debug(msg=f"Package: {record.small_id} , action: {record.action}"
                                      f", pipeline: {record.pipeline_id}, timestamp: {record.time_stamp}")

        elif isinstance(data, PathRecordDict):
            record = PathRecord(
                parcel_id=self.parcel_id,
                small_id=self.small_id,
                parcel_type=self.parcel_type,
                ident_des_zno=self.ident_des_zno,
                sorter_type=self.sorter_type,
                dest_type=self.dest_type,
                **data,
            )

            self.path_request_data.append(record)
            self.data_pipeline.put(record)

            LOG.logger_font.debug(msg=f"Package get path - parcel_id: {record.parcel_id}, small_id: {record.small_id}, "
                                      f", path: {record.ret_path}"
                                      f", parcel_type: {record.parcel_type}, ident_des_zno: {record.ident_des_zno}"
                                      f", sorter_type: {record.sorter_type}, dest_type: {record.dest_type}")

        else:
            raise ValueError("Wrong type of record")

    def pop_mark(self):
        """删去第一个节点, 返回下一个 pipeline id: (now_loc, next_loc)"""
        self.path.pop(0)
        if len(self.path) >= 2:
            self.next_pipeline = tuple(self.path[0: 2])
        # 当 package 去到 reload（终分拣）， 终分拣的队列 id 只有一个值
        elif len(self.path) == 1:
            self.next_pipeline = self.path[-1]
        else:
            raise ValueError('The path have been empty!')

    def __str__(self):
        display_dct = dict(self.attr)
        return f"<Package attr:{dict(display_dct)}, path: {self.planned_path}>"

    __repr__ = __str__


class Parcel(Package):
    """包裹"""

    def __init__(self,
                 attr: pd.Series,
                 data_pipeline: Queue):
        # add for Package class compatible
        super(Parcel, self).__init__(attr, data_pipeline)

    def __str__(self):
        display_dct = dict(self.attr)
        return f"<Parcel attr:{dict(display_dct)}>"


class SmallPackage(Package):
    """小件包裹"""
    def __init__(self,
                 attr: pd.Series,
                 data_pipeline: Queue):
        # add for Package class compatible
        super(SmallPackage, self).__init__(attr, data_pipeline)

    def __str__(self):
        display_dct = dict(self.attr)
        return f"<SmallPackage attr:{dict(display_dct)}>"


class SmallBag(Package):
    """小件包"""
    def __init__(self,
                 small_packages,
                 data_pipeline: Queue):
        # random choice a small_packages as attr
        attr = random.choice(small_packages).attr
        super(SmallBag, self).__init__(attr, data_pipeline)

        # 存储小件包裹
        self.store = small_packages
        self.store_size = len(self.store)

    @property
    def parcel_id(self):
        return self._parcel_id

    @parcel_id.setter
    def parcel_id(self, value: str):
        self._parcel_id = value
        # parcel id 更新到小件包里的小件包裹
        for x in self.store:
            x.parcel_id = value

    def get_all_package(self):
        return [self.store.pop(0) for _ in range(self.store_size)]

    def insert_data(self, data: dict, to_small: bool=True):
        """给小件包裹添加记录"""
        if to_small:
            list(map(lambda x: x.insert_data(data), self.store))
        return super(SmallBag, self).insert_data(data)

    def __str__(self):
        display_dct = dict(self.attr)
        return f"<SmallBag attr:{dict(display_dct)}, path: {self.planned_path}, store_size:{self.store_size}>"


class Truck:
    """货车"""
    def __init__(self, truck_id: str, come_time: int, truck_type: str, packages: list, data_pipeline: Queue):
        """
        :param truck_id: self explain
        :param come_time: self explain
        :param packages: a data frame contain all packages
        """
        self.truck_id = truck_id
        self.come_time = come_time
        self.store = packages
        self.truck_type = truck_type
        self.truck_data = list()
        # 仿真程序运行的同时，消费数据
        self.data_pipeline = data_pipeline
        self.store_size = len(self.store)

    def get_all_package(self):
        return [self.store.pop(0) for _ in range(self.store_size)]

    def insert_data(self, data:dict):
        assert isinstance(data, TruckRecordDict), "Wrong data type"
        record = TruckRecord(
                    truck_id=self.truck_id,
                    truck_type=self.truck_type,
                    store_size=self.store_size,
                    **data,)

        LOG.logger_font.debug(msg=f"Truck: {record}")

        self.truck_data.append(record)
        self.data_pipeline.put(record)

    def __str__(self):
        return f"<Truck truck_id: {self.truck_id}, come_time: {self.come_time}, store_size:{self.store_size}>"

    __repr__ = __str__


class Uld(Truck):
    """航空箱"""
    pass


class BasePipeline:
    """基础管道，收集垃圾，或者错误"""
    def __init__(self,
                 env: simpy.Environment,
                 pipeline_id: str,
                 equipment_id: str,
                 machine_type: str,
                 is_record:bool = True):

        self.env = env
        self.pipeline_id = pipeline_id
        self.equipment_id = equipment_id
        self.queue_id = pipeline_id
        self.machine_type = machine_type
        self.is_record = is_record
        self.queue = simpy.Store(env)

    def get(self):
        return self.queue.get()

    def put(self, item):
        # control writing record
        if self.is_record:
            item.insert_data(
                PipelineRecordDict(
                    pipeline_id=self.pipeline_id,  # pipeline name : unload_error / small_bin
                    queue_id=self.queue_id,
                    time_stamp=self.env.now,
                    action="start", ))

        self.queue.put(item)

    def __str__(self):
        return f"<Pipeline: {self.pipeline_id}>"

    __repr__ = __str__


class Pipeline:

    """传送带"""

    def __init__(self,
                 env: simpy.Environment,
                 delay_time: float,
                 pipeline_id: tuple,
                 queue_id: str,
                 machine_type: str,
                 open_time_dict: dict,
                 all_keep_open: bool,
                 ):

        self.env = env
        self.delay = delay_time

        # store for put in the front
        # queue for get in the end
        self.store = simpy.Store(env)
        self.queue = simpy.Store(env)

        self.pipeline_id = pipeline_id
        self.queue_id = queue_id
        self.machine_type = machine_type
        self.equipment_id = self.pipeline_id[1]  # in Pipeline the equipment_id is equipment after this pipeline

        # open close time table
        self.open_time = open_time_dict.get(self.equipment_id, [])
        self.open_time_cp = tuple(self.open_time)

        self.keep_open = all_keep_open

    def latency(self, item: Package):

        """模拟传送时间"""
        # pipeline start server
        item.insert_data(
            PipelineRecordDict(
                pipeline_id=':'.join(self.pipeline_id),
                queue_id=self.queue_id,
                time_stamp=self.env.now,
                action="start", ))

        # re cal the wait time stamp
        t_pipeline_start = self.env.now
        item_last_end_time = item.machine_data[-1].time_stamp
        wait_machine_open_gap = t_pipeline_start - item_last_end_time

        yield self.env.timeout(self.delay)
        # cutting path
        item.pop_mark()

        # package wait for next process
        item.insert_data(
            PackageRecordDict(
                equipment_id=self.equipment_id,
                time_stamp=(self.env.now - wait_machine_open_gap),
                action="wait", ))

        # pipeline end server
        item.insert_data(
            PipelineRecordDict(
                pipeline_id=':'.join(self.pipeline_id),
                queue_id=self.queue_id,
                time_stamp=self.env.now,
                action="end", ))

        self.queue.put(item)

    def put(self, item: Package):
        self.store.put(item)

    def get(self):
        return self.queue.get()

    def run(self):
        """setup process"""
        yield self.env.timeout(0)

        if self.keep_open:
            self.env.process(self.all_run())

        else:
            for start, end in self.open_time:
                self.env.process(self.real_run(start, end))

    def all_run(self):
        while True:
            item = yield self.store.get()
            self.env.process(self.latency(item))

    def real_run(self, start, end):

        yield self.env.timeout(start)

        while True:
            item = yield self.store.get()
            LOG.logger_font.debug(f"sim time: {self.env.now}, get item: {item}, equipment_id: {self.equipment_id}")

            if self.env.now > end:
                self.store.put(item)
                LOG.logger_font.debug(f"sim time: {self.env.now}, put back item: {item}, equipment_id: {self.equipment_id}")
                self.env.exit()

            self.env.process(self.latency(item))

    def __str__(self):
        return f"<Pipeline: {self.pipeline_id}, delay: {self.delay}>"

    __repr__ = __str__


class PipelineReplace(Pipeline):

    """共享队列的传送带"""

    def __init__(self,
                 env: simpy.Environment,
                 delay_time: float,
                 pipeline_id: tuple,
                 queue_id: str,
                 machine_type: str,
                 share_store_dict: dict,
                 equipment_store_dict: dict,
                 open_time_dict: dict,
                 all_keep_open: bool,
                 ):

        super(PipelineReplace, self).__init__(env,
                                              delay_time,
                                              pipeline_id,
                                              queue_id,
                                              machine_type,
                                              open_time_dict,
                                              all_keep_open,)

        self.share_store_dict = share_store_dict
        self.equipment_store_dict = equipment_store_dict

        # replace self.queue
        self.share_store_id = self.equipment_store_dict[self.equipment_id]
        self.store = self.share_store_dict[self.share_store_id]

    def __str__(self):
        return f"<PipelineReplaceJ: {self.pipeline_id}, delay: {self.delay}>"


class PipelineRes(Pipeline):

    def __init__(self,
                 env: simpy.Environment,
                 resource_dict: defaultdict,
                 equipment_resource_dict: dict,
                 delay_time: float,
                 pipeline_id: tuple,
                 queue_id: str,
                 machine_type: str,
                 equipment_process_time_dict: dict,
                 open_time_dict: dict,
                 all_keep_open: bool,
                 ):

        super(PipelineRes, self).__init__(env,
                                          delay_time,
                                          pipeline_id,
                                          queue_id,
                                          machine_type,
                                          open_time_dict,
                                          all_keep_open)

        self.equipment_last = self.pipeline_id[0]  # in PipelineRes the equipment_id is equipment before this pipeline
        self.equipment_next = self.pipeline_id[1]  # in PipelineRes the equipment_id is equipment before this pipeline
        self.resource_id = equipment_resource_dict[self.equipment_last]
        self.resource = resource_dict[self.resource_id]["resource"]
        # add for equipment
        self.equipment_process_time_dict = equipment_process_time_dict
        self.process_time = self.equipment_process_time_dict[self.equipment_last]

    def latency(self, item: Package):

        with self.resource.request() as req:
            """模拟传送时间"""

            yield req

            # package start for process
            item.insert_data(
                PackageRecordDict(
                    equipment_id=self.equipment_last,
                    time_stamp=self.env.now,
                    action="start", ))

            yield self.env.timeout(self.process_time)

            # package end for process
            item.insert_data(
                PackageRecordDict(
                    equipment_id=self.equipment_last,
                    time_stamp=self.env.now,
                    action="end", ))

            # pipeline start server
            item.insert_data(
                PipelineRecordDict(
                    pipeline_id=':'.join(self.pipeline_id),
                    queue_id=self.queue_id,
                    time_stamp=self.env.now,
                    action="start", ))

            yield self.env.timeout(self.delay)

            # package start for process
            item.insert_data(
                PackageRecordDict(
                    equipment_id=self.equipment_next,
                    time_stamp=self.env.now,
                    action="wait", ))

            # pipeline end server
            item.insert_data(
                PipelineRecordDict(
                    pipeline_id=':'.join(self.pipeline_id),
                    queue_id=self.queue_id,
                    time_stamp=self.env.now,
                    action="end", ))

            # cutting path, change item next_pipeline
            item.pop_mark()
            self.queue.put(item)

    def __str__(self):
        return f"<PipelineRes: {self.pipeline_id}, delay: {self.delay}>"


if __name__ == '__main__':
    pass
