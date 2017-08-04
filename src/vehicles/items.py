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

from collections import namedtuple, defaultdict
from src.utils import PackageRecord, PipelineRecord, TruckRecord
from src.controllers import PathGenerator
from src.config import LOG

__all__ = ["Package", "Truck", "Uld", "SmallBag", "SmallPackage", "Pipeline", "PipelineRes", "BasePipeline"]

# init path generator
path_generator = PathGenerator()


class Package:
    """包裹"""
    def __init__(self,
                 env: simpy.Environment,
                 attr: pd.Series,):

        # 包裹的所有信息都在 attr
        self.attr = attr
        # id
        self.item_id = self.attr["parcel_id"]
        # env
        self.env = env
        # data store
        self.machine_data = []
        self.pipeline_data = []
        # path_generator
        self.path_generator = path_generator.path_generator
        # paths
        self.planned_path = None
        self.path = None
        # next pipeline_id
        self.next_pipeline = None

        self.ident_des_zno = self.attr["ident_des_zno"]
        self.dest_type = self.attr["dest_type"]
        self.parcel_type = self.attr["parcel_type"]
        self.sorter_type = "reload" if self.parcel_type == "parcel" else "small_sort"

    # use in unload machine
    def set_path(self, package_start):
        path = path_generator.path_generator(package_start, self.ident_des_zno, self.sorter_type, self.dest_type)
        self.planned_path = tuple(path)
        self.path = list(self.planned_path)
        self.next_pipeline = self.planned_path[:2]

    def insert_data(self, record: namedtuple):
        # print out data
        if isinstance(record, PackageRecord):
            self.machine_data.append(record)

            LOG.logger_font.debug(msg=f"Package: {record.package_id} , action: {record.action}"
                             f", equipment: {record.equipment_id}, timestamp: {record.time_stamp}")

        elif isinstance(record, PipelineRecord):
            self.pipeline_data.append(record)

            LOG.logger_font.debug(msg=f"Package: {record.package_id} , action: {record.action}"
                              f", pipeline: {record.pipeline_id}, timestamp: {record.time_stamp}")

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
        # remove the now_loc
        # 改变下一个 pipeline id

    def __str__(self):
        display_dct = dict(self.attr)
        return f"<package attr:{dict(display_dct)}, path: {self.planned_path}>"


class SmallPackage(Package):
    """小件包裹"""
    def __init__(self,
                 env: simpy.Environment,
                 attr: pd.Series,):

        super(SmallPackage, self).__init__(env, attr,)
        self.item_id = self.attr["small_id"]
        # env
        self.env = env

    def __str__(self):
        display_dct = dict(self.attr)
        return f"<SmallBag attr:{dict(display_dct)}>"


class SmallBag(Package):
    """小件包"""
    def __init__(self, env: simpy.Environment,
                 attr: pd.Series,
                 small_packages: list):

        super(SmallBag, self).__init__(env, attr,)

        # 存储小件包裹
        self.store = small_packages
        self.store_size = len(self.store)

    def insert_data_small(self, record: namedtuple):
        """给小件包裹添加记录"""
        map(lambda x: x.instert_data(record), self.store)

    def __str__(self):
        display_dct = dict(self.attr)
        return f"<SmallBag attr:{dict(display_dct)}, path: {self.planned_path}, store_size:{self.store_size}>"


class Truck:
    """货车"""
    def __init__(self, env: simpy.Environment, item_id: str, come_time: int, truck_type: str, packages: list):
        """
        :param truck_id: self explain
        :param come_time: self explain
        :param packages: a data frame contain all packages
        """
        self.item_id = item_id
        self.come_time = come_time
        self.store = packages
        assert self._all_are_packages(), "Truck store Package only !!"
        self.store_size = len(self.store)
        self.truck_type = truck_type
        self.env = env
        self.truck_data = []

    def _all_are_packages(self):
        packages_bool = [isinstance(package, Package) for package in self.store]
        return all(packages_bool)

    def insert_data(self, record: namedtuple):

        if isinstance(record, TruckRecord):
            self.truck_data.append(record)
        else:
            raise ValueError("Wrong type of record")

    def __str__(self):
        return f"<truck_id: {self.item_id}, come_time: {self.come_time}, store_size:{self.store_size}>"


class Uld(Truck):
    """航空箱"""
    pass


class BasePipeline:

    def __init__(self, env: simpy.Environment, pipeline_id: str, equipment_id: str, machine_type: str, ):

        self.env = env
        self.pipeline_id = pipeline_id
        self.equipment_id = equipment_id
        self.queue_id = pipeline_id
        self.machine_type = machine_type
        self.queue = simpy.Store(env)

    def get(self):
        return self.queue.get()

    def put(self, item):

        item.insert_data(
            PipelineRecord(
                pipeline_id=self.pipeline_id,  # pipeline name : unload_error
                queue_id=self.queue_id,
                package_id=item.item_id,
                time_stamp=self.env.now,
                action="start", ))

        self.queue.put(item)


class Pipeline:

    """传送带"""

    def __init__(self,
                 env: simpy.Environment,
                 delay_time: float,
                 pipeline_id: tuple,
                 queue_id: str,
                 machine_type: str,
                 ):

        self.env = env
        self.delay = delay_time
        self.queue = simpy.Store(env)
        self.pipeline_id = pipeline_id
        self.queue_id = queue_id
        self.machine_type = machine_type
        self.equipment_id = self.pipeline_id[1]  # in Pipeline the equipment_id is equipment after this pipeline

    def latency(self, item: Package):
        """模拟传送时间"""

        # pipeline start server
        item.insert_data(
            PipelineRecord(
                pipeline_id=':'.join(self.pipeline_id),
                queue_id=self.queue_id,
                package_id=item.item_id,
                time_stamp=self.env.now,
                action="start", ))

        yield self.env.timeout(self.delay)
        # cutting path
        item.pop_mark()

        # package wait for next process
        item.insert_data(
            PackageRecord(
                equipment_id=self.equipment_id,
                package_id=item.item_id,
                time_stamp=self.env.now,
                action="wait", ))

        # pipeline end server
        item.insert_data(
            PipelineRecord(
                pipeline_id=':'.join(self.pipeline_id),
                queue_id=self.queue_id,
                package_id=item.item_id,
                time_stamp=self.env.now,
                action="end", ))

        self.queue.put(item)

    def put(self, item: Package):
        self.env.process(self.latency(item))

    def get(self):
        return self.queue.get()

    def __str__(self):
        return f"<Pipeline: {self.pipeline_id}, delay: {self.delay}>"


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
                 ):

        super(PipelineRes, self).__init__(env,
                                          delay_time,
                                          pipeline_id,
                                          queue_id,
                                          machine_type,)

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
                PackageRecord(
                    equipment_id=self.equipment_last,
                    package_id=item.item_id,
                    time_stamp=self.env.now,
                    action="start", ))

            yield self.env.timeout(self.process_time)

            # package end for process
            item.insert_data(
                PackageRecord(
                    equipment_id=self.equipment_last,
                    package_id=item.item_id,
                    time_stamp=self.env.now,
                    action="end", ))

            # pipeline start server
            item.insert_data(
                PipelineRecord(
                    pipeline_id=':'.join(self.pipeline_id),
                    queue_id=self.queue_id,
                    package_id=item.item_id,
                    time_stamp=self.env.now,
                    action="start", ))

            yield self.env.timeout(self.delay)

            # package start for process
            item.insert_data(
                PackageRecord(
                    equipment_id=self.equipment_next,
                    package_id=item.item_id,
                    time_stamp=self.env.now,
                    action="wait", ))

            # pipeline end server
            item.insert_data(
                PipelineRecord(
                    pipeline_id=':'.join(self.pipeline_id),
                    queue_id=self.queue_id,
                    package_id=item.item_id,
                    time_stamp=self.env.now,
                    action="end", ))

            # cutting path, change item next_pipeline
            item.pop_mark()
            self.queue.put(item)


if __name__ == '__main__':
    pass
