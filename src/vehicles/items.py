# -*- coding: utf-8 -*-

"""
作者：
日期：
说明：

包裹 class
货物 class
Uld class

"""
import simpy
import pandas as pd
from collections import

__all__ = ["Package", "Truck", "Uld", "SmallBag", "SmallPackage", "Pipeline"]


# todo: add test instance in the end of the file, using path generator


class Package:

    def __init__(self, env: simpy.Environment, attr: pd.Series, item_id : str, path: tuple, ):

        self.attr = attr
        # id
        self.item_id = item_id
        # env
        self.env = env
        # for record
        self.plan_path = path
        # for popping
        self.path = list(path)
        # for time
        self.time_records = []


    def ret_pop_mark(self):

        """return next pipeline id, pop the first element of plan_path, marking the time"""

        if len(self.plan_path) >= 2:
            now_loc = self.plan_path[0]
            next_loc = self.plan_path[1]
        else:
            raise ValueError('The path have been empty!')

        pop_loc = self.plan_path.pop(0)
        self.time_records.append((pop_loc, self.env.now))

        return now_loc, next_loc


    def __str__(self):
        display_dct = dict(self.attr)
        return f"<package attr:{dict(display_dct)}, path: {self.plan_path}>"


class SmallBag(Package):

    def __str__(self):
        display_dct = dict(self.attr)
        return f"<SmallBag attr:{dict(display_dct)}, path: {self.plan_path}>"


class SmallPackage(Package):

    def __str__(self):
        display_dct = dict(self.attr)
        return f"<SmallBag attr:{dict(display_dct)}, path: {self.plan_path}>"



# vehicles

class Truck:

    def __init__(self, env: simpy.Environment, item_id, come_time, packages:pd.DataFrame):
        """
        :param truck_id: self explain
        :param come_time: self explain
        :param packages: a dataframe contain all packages
        """
        self.item_id = item_id
        self.come_time = come_time
        self.store = packages
        self.env = env

    def __str__(self):
        """
        :return:
        """
        return f"<truck_id: {self.item_id}, come_time: {self.come_time}, store_size:{len(self.store)}>"


class Uld(Truck):
    pass


class Pipeline:

    """传送带"""

    def __init__(self,
                 env: simpy.Environment,
                 delay_time: float,
                 pipeline_id: tuple,
                 queue_id: str,
                 ):

        self.env = env
        self.delay = delay_time
        self.queue = simpy.PriorityStore(env)
        self.pipeline_id = pipeline_id
        self.queue_id = queue_id
        self.package_counts = 0
        self.package_counts_time = []
        # 加入计数器
        self.env.process(self.get_counts())

    def get_counts(self):
        """计数器"""
        while True:
            self.env.timeout(1)
            self.package_counts_time.append((self.env.now, self.package_counts))

    def latency(self, item: Package):
        """模拟传送时间"""
        yield self.env.timeout(self.delay)
        self.queue.put(simpy.PriorityItem(priority=self.env.now,
                                          item=item))

    def put(self, item: Package):
        self.package_counts += 1
        self.env.process(self.latency(item))

    def get(self):
        self.package_counts -= 1
        return self.queue.get()

    def __str__(self):
        return f"<Pipeline: {self.pipeline_id}, delay: {self.delay}, package_counts: {self.package_counts}>"