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

from collections import namedtuple
from src.utils import PackageRecord, PipelineRecord, TruckRecord

__all__ = ["Package", "Truck", "Uld", "SmallBag", "SmallPackage", "Pipeline"]


class Package:
    """包裹"""
    def __init__(self,
                 env: simpy.Environment,
                 attr: pd.Series,
                 item_id : str,
                 path: tuple, ):

        # 包裹的所有信息都在 attr
        self.attr = attr
        # id
        self.item_id = item_id
        # env
        self.env = env
        # for record
        self.plan_path = path
        # for popping
        self.path = list(path)
        # next pipeline_id
        self.next_pipeline = ()

        self.machine_data = []
        self.pipeline_data = []

    def instert_data(self, record: namedtuple):

        if isinstance(record, PackageRecord):
            self.machine_data.append(record)
        elif isinstance(record, PipelineRecord):
            self.pipeline_data.append(record)
        else:
            raise ValueError("Wrong type of record")

    def pop_mark(self):
        """返回下一个pipeline id: (now_loc, next_loc)， 删去第一个节点，记录当前的时间点"""
        if len(self.path) >= 2:
            now_loc, next_loc = self.path[0: 2]
        # 当 package 去到 reload（终分拣）， 终分拣的队列 id 只有一个值
        elif len(self.path) == 1:
            now_loc, next_loc = self.path[-1], None
        else:
            raise ValueError('The path have been empty!')
        # remove the now_loc
        self.path.pop(0)
        # 改变下一个 pipeline id
        self.next_pipeline = now_loc, next_loc

    def __str__(self):
        display_dct = dict(self.attr)
        return f"<package attr:{dict(display_dct)}, path: {self.plan_path}>"


class SmallPackage(Package):
    """小件包裹"""
    def __str__(self):
        display_dct = dict(self.attr)
        return f"<SmallBag attr:{dict(display_dct)}, path: {self.plan_path}>"


class SmallBag(Package):
    """小件包"""
    # todo
    def __init__(self, env: simpy.Environment,
                 attr: pd.Series,
                 item_id : str,
                 path: tuple,
                 small_packages: pd.DataFrame):

        super(SmallBag, self).__init__(env, attr, item_id, path)

        self.store = small_packages
        self.store_size = len(self.store)

    def __str__(self):
        display_dct = dict(self.attr)
        return f"<SmallBag attr:{dict(display_dct)}, path: {self.plan_path}, store_size:{store_size}>"


class Truck:
    """货车"""
    def __init__(self, env: simpy.Environment, item_id: str, come_time: int, truck_type: str, packages:pd.DataFrame):
        """
        :param truck_id: self explain
        :param come_time: self explain
        :param packages: a dataframe contain all packages
        """
        self.item_id = item_id
        self.come_time = come_time
        self.store = packages
        self.store_size = len(self.store)
        self.truck_type = truck_type
        self.env = env

        self.truck_data = []

    def instert_data(self, record: namedtuple):

        if isinstance(record, TruckRecord):
            self.truck_data.append(record)
        else:
            raise ValueError("Wrong type of record")

    def __str__(self):
        return f"<truck_id: {self.item_id}, come_time: {self.come_time}, store_size:{self.store_size}>"


class Uld(Truck):
    """航空箱"""
    pass


class Pipeline:

    """传送带"""

    def __init__(self,
                 env: simpy.Environment,
                 delay_time: float=0,
                 pipeline_id: tuple=None,
                 queue_id: str=None,
                 machine_type: str=None,
                 ):

        self.env = env
        self.delay = delay_time
        self.queue = simpy.Store(env)
        self.pipeline_id = pipeline_id
        self.queue_id = queue_id
        self.machine_type = machine_type

    def latency(self, item: Package):
        """模拟传送时间"""
        yield self.env.timeout(self.delay)
        # cutting path
        item.pop_mark()
        # insert data

        item.instert_data(
            PackageRecord(
                machine_id=self.pipeline_id,
                package_id=item.item_id,
                time_stamp=self.env.now,
                action="wait", ))

        item.instert_data(
            PipelineRecord(
                pipeline_id=self.pipeline_id,
                package_id=item.item_id,
                time_stamp=self.env.now,
                action="end", ))

        self.queue.put(item)

    def put(self, item: Package):

        item.instert_data(
            PipelineRecord(
                pipeline_id=self.pipeline_id,
                package_id=item.item_id,
                time_stamp=self.env.now,
                action="start", ))

        self.env.process(self.latency(item))

    def get(self):
        return self.queue.get()

    def __str__(self):
        return f"<Pipeline: {self.pipeline_id}, delay: {self.delay}, package_counts: {self.latency_counts}>"

if __name__ == '__main__':
    pass

