# -*- coding: utf-8 -*-

"""
作者：
日期：
说明：

存放车辆的控制器，机器及队列的监视器

"""
import simpy
import pandas as pd
import numpy as np

from simpy_lib.hangzhou_simpy.src.vehicles import Truck, SmallPackage, SmallBag, Parcel, Pipeline
from simpy_lib.hangzhou_simpy.src.utils import TruckRecordDict
from simpy_lib.hangzhou_simpy.src.db import get_vehicles, get_resource_timetable, get_equipment_timetable
from simpy_lib.hangzhou_simpy.src.config import LOG


__all__ = ["TruckController", "ResourceController"]


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
        truck = Truck(truck_id=truck_id, come_time=come_time,
                      packages=packages, truck_type=truck_type, )
        LOG.logger_font.debug(f"init truck: {truck_id}")
        self.env.process(self.latency(come_time, truck))

    def controller(self):
        """
        """
        for keys, packages_record in self.trucks_dict.items():
            self.env.process(self._init_truck(keys, packages_record))


class ResourceController:
    """control resource change during simulation"""
    def __init__(self,
                 env: simpy.Environment,
                 resource_dict,):

        self.env = env
        self.resource_dict = resource_dict
        self.until_death = self.env.timeout(1_000_000_000)

        self._init_time_table()

    def _init_time_table(self):
        self.timetable = get_resource_timetable()

    def _set_resource(self, resource: simpy.PriorityResource, start_time: float, end_time: float):
        """占用资源，模拟资源减少的情况"""
        yield self.env.timeout(start_time)

        with resource.request(priority=-1) as req:
            yield req

            if end_time != np.inf:
                duration = end_time - start_time
                yield self.env.timeout(duration)
            else:
                # all machine finished
                yield self.until_death

    def controller(self):
        for _, row in self.timetable.iterrows():

            # load data
            resource_id = row['resource_id']
            start_time = row['start_time']
            end_time = row['end_time']
            resource_occupy = row['resource_occupy']
            # 资源
            resource = self.resource_dict[resource_id]["resource"]
            # 占用进程
            for _ in range(int(resource_occupy)):
                self.env.process(self._set_resource(resource, start_time=start_time, end_time=end_time))


if __name__ == '__main__':
    pass