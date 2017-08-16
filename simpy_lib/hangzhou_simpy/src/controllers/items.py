# -*- coding: utf-8 -*-

"""
作者：
日期：
说明：

存放车辆的控制器，机器及队列的监视器

"""

import simpy
import pandas as pd
from simpy_lib.hangzhou_simpy.src.vehicles import Truck, Package, SmallPackage, SmallBag, Parcel
from simpy_lib.hangzhou_simpy.src.utils import TruckRecordDict
from simpy_lib.hangzhou_simpy.src.db import get_vehicles
from simpy_lib.hangzhou_simpy.src.config import LOG

__all__ = ["TruckController", ]


class TruckController:

    def __init__(self,
                 env: simpy.Environment,
                 trucks: simpy.FilterStore,
                 is_test: bool,
                 is_parcel_only: bool,
                 is_land_only:bool,):

        self.env = env
        self.trucks = trucks
        self.is_test = is_test
        self.is_parcel_only = is_parcel_only
        self.is_land_only = is_land_only
        self._init_truck_data()

    def _init_truck_data(self):

        trucks_dict, truck_small_dict = get_vehicles(is_test=self.is_test,
                                                     is_land=True,
                                                     is_parcel_only=self.is_parcel_only)

        if not self.is_land_only:
            uld_dict, uld_small_dict = get_vehicles(is_test=self.is_test,
                                                    is_land=False,
                                                    is_parcel_only=self.is_parcel_only)
            trucks_dict.update(uld_dict)
            truck_small_dict.update(uld_small_dict)

        self.trucks_dict = trucks_dict
        self.truck_small_dict = truck_small_dict

    @staticmethod
    def _init_package(cls: type, package_record: pd.Series):
        return cls(attr=package_record)

    def _init_small_bag(self, small_bag_record: pd.Series):
        parcel_id = small_bag_record["parcel_id"]
        small_package_records = self.truck_small_dict[parcel_id]
        small_packages = [self._init_package(cls=SmallPackage, package_record=record) for _, record in small_package_records.iterrows()]
        return SmallBag(small_packages=small_packages)

    def latency(self, come_time, item: Truck):
        """模拟货车到达时间"""
        yield self.env.timeout(come_time)

        item.insert_data(TruckRecordDict(
                             equipment_id="truck",
                             time_stamp=self.env.now,
                             action="wait",))

        # truck start enter
        self.trucks.put(item)

    def _init_truck(self, keys: tuple, packages_record: pd.DataFrame):

        yield self.env.timeout(0)
        # init packages
        packages = list()
        for _, package_record in packages_record.iterrows():
            parcel_type = package_record['parcel_type']

            if parcel_type in ['parcel', 'nc']:
                package = self._init_package(cls=Parcel, package_record=package_record)
            elif parcel_type == 'small':
                package = self._init_small_bag(small_bag_record=package_record)
            else:
                raise ValueError("parcel_type can only be parcel/small/nc!!")

            packages.append(package)

        # init truck
        (truck_id, come_time, src_type,) = keys
        # find out package dest_type
        package_dest_type = 'A' if 'A' in list(set(package.dest_type for package in packages)) else 'L'
        # LL/LA/AA/AA
        truck_type = src_type + package_dest_type
        truck = Truck(item_id=truck_id, come_time=come_time,
                      packages=packages, truck_type=truck_type,)
        LOG.logger_font.debug(f"init truck: {truck_id}")
        self.env.process(self.latency(come_time, truck))

    def controller(self):
        """
        """
        for keys, packages_record in self.trucks_dict.items():
            self.env.process(self._init_truck(keys, packages_record))


if __name__ == '__main__':
    pass