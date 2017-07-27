# -*- coding: utf-8 -*-

"""
作者：
日期：
说明：

存放车辆的控制器，机器及队列的监视器

"""
import simpy

import pandas as pd
from src.vehicles import Truck, Package, SmallPackage, SmallBag
from src.utils import TruckRecord
from src.db import get_vehicles
import logging


__all__ = ["TruckController", ]

# todo:


class TruckController:

    def __init__(self, env: simpy.Environment, trucks: simpy.FilterStore, is_test: bool=False):

        self.env = env
        self.trucks = trucks
        self.is_test = is_test
        self._init_truck_data()

    def _init_truck_data(self):

        trucks_dict, truck_small_dict = get_vehicles(is_test=self.is_test, is_land=True)
        uld_dict, uld_small_dict = get_vehicles(is_test=self.is_test, is_land=False)

        trucks_dict.update(uld_dict)
        truck_small_dict.update(uld_small_dict)

        self.trucks_dict = trucks_dict
        self.truck_small_dict = truck_small_dict

    def _init_package(self, cls: type, package_record: pd.Series):
        return cls(env=self.env, attr=package_record)

    def _init_small_bag(self, small_bag_record: pd.Series):
        parcel_id = small_bag_record.get("parcel_id")
        small_package_records = self.truck_small_dict.get(parcel_id, [])
        small_packages = [self._init_package(cls=SmallPackage, package_record=record) for record in small_package_records]
        return SmallBag(env=self.env, attr=small_bag_record, small_packages=small_packages)

    def latency(self, come_time, item: Truck):
        """模拟货车到达时间"""
        yield self.env.timeout(come_time)

        item.insert_data(
            TruckRecord(
                equipment_id="truck",
                truck_id=item.item_id,
                time_stamp=self.env.now,
                action="wait",
                store_size=item.store_size,))

        # truck start enter
        self.trucks.put(item)

    def controller(self):
        """
        """

        for keys, packages_record in self.trucks_dict.items():

            # init packages
            packages = list()
            for _, package_record in packages_record.iterrows():
                parcel_type = package_record['parcel_type']

                if parcel_type == 'parcel':
                    package = self._init_package(cls=Package, package_record=package_record)
                elif parcel_type == 'small':
                    package = self._init_small_bag(small_bag_record=package_record)
                else:
                    raise ValueError("parcel_type is either parcel or small!!")

                packages.append(package)

            # init truck
            (truck_id, come_time, truck_type,) = keys
            truck = Truck(env=self.env, item_id=truck_id, come_time=come_time,
                          packages=packages, truck_type=truck_type,
                          )
            self.env.process(self.latency(come_time, truck))

if __name__ == '__main__':
    pass
