# -*- coding: utf-8 -*-

"""
作者：
日期：
说明：

存放车辆的控制器，机器及队列的监视器

"""
import simpy

from src.vehicles import Truck
from src.db import get_trucks


__all__ = ["TruckController", ]


class TruckController:

    def __init__(self, env: simpy.Environment, trucks: simpy.FilterStore):

        self.env = env
        self.trucks = trucks

    def latency(self, come_time, item: Truck):
        """模拟货车到达时间"""
        yield self.env.timeout(come_time)
        self.trucks.put(item)

    def controller(self):
        """
        des: 使用 FilterStore 特定的车辆筛选进不同的 r 入口
        """
        trucks_dict = get_trucks()

        for (truck_id, come_time, truck_type), packages in trucks_dict:
            truck = Truck(item_id=truck_id, come_time=come_time,
                          packages=packages, truck_type=truck_type, )

            self.env.process(self.latency(come_time, truck))

if  __name__ == '__main__':
    pass