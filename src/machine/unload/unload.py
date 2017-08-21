# -*- coding: utf-8 -*-


"""
author: Ted
date: 2017-07-11
des:

unload modules
"""

import simpy

from collections import defaultdict
from src.machine import BaseMachine
from src.vehicles import Package, Truck
from src.config import LOG
from src.utils import PackageRecordDict, TruckRecordDict


class Unload(BaseMachine):

    def __init__(self,
                 env: simpy.Environment,
                 machine_id: str,
                 unload_setting_dict: dict,
                 reload_setting_dict: dict,
                 trucks_q: simpy.FilterStore,
                 done_trucks_q: simpy.Store,
                 pipelines_dict: dict,
                 resource_dict: defaultdict,
                 equipment_resource_dict: dict,
                 equipment_parameters: dict
                 ):

        super(Unload, self).__init__(env)

        self.machine_id = machine_id
        self.unload_setting_dict = unload_setting_dict
        self.reload_setting_dict = reload_setting_dict
        self.trucks_q = trucks_q
        self.done_trucks_q = done_trucks_q
        self.pipelines_dict = pipelines_dict
        self.resource_dict = resource_dict
        self.equipment_resource_dict = equipment_resource_dict
        self.equipment_parameters = equipment_parameters

        # add machine switch
        self.machine_switch = self.env.event()
        self.machine_switch.succeed()

        self.resource_set = self._set_machine_resource()

    def _set_machine_resource(self):
        """"""
        if self.equipment_resource_dict:
            # pipeline id last value, for other machines (r1_1, etc)
            self.equipment_id = self.machine_id
            self.equipment_name = self.machine_id.split('_')[0]  # r1, ect
            self.resource_id = self.equipment_resource_dict[self.equipment_id]
            self.resource = self.resource_dict[self.resource_id]['resource']
            self.process_time = self.resource_dict[self.resource_id]['process_time']
            self.truck_types = self.unload_setting_dict[self.equipment_id]
            self.vehicle_turnaround_time = self.equipment_parameters[self.equipment_name]["vehicle_turnaround_time"]

        else:
            raise RuntimeError('unload machine',
                               self.machine_id,
                               'not initial equipment_resource_dict!')

    def process_package(self, package: Package):
        """处理单个包裹"""
        with self.resource.request() as req:
            yield req

            package.insert_data(
                PackageRecordDict(
                    equipment_id=self.equipment_id,
                    time_stamp=self.env.now,
                    action="start", ))

            yield self.env.timeout(self.process_time)

            package.insert_data(
                PackageRecordDict(
                    equipment_id=self.equipment_id,
                    time_stamp=self.env.now,
                    action="end", ))

            # deal with nc parcel
            if package.attr['parcel_type'] == 'nc':
                self.pipelines_dict["unload_error"].put(package)
            else:
                # error package store in
                try:
                    package.set_path(package_start=self.machine_id)
                    self.pipelines_dict[package.next_pipeline].put(package)
                except Exception as exc:
                    msg = f"error: {exc}, package: {package}, reload_port: {self.equipment_id}"
                    LOG.logger_font.error(msg)
                    LOG.logger_font.exception(exc)
                    self.pipelines_dict["unload_error"].put(package)

    def process_truck(self, truck: Truck):
        """process one truck"""
        packages = truck.get_all_package()

        events_processes = list()
        for package in packages:
            # add package wait data
            package.insert_data(
                PackageRecordDict(
                    equipment_id=self.equipment_id,
                    time_stamp=truck.come_time,
                    action="wait", ))

            events_processes.append(self.env.process(self.process_package(package)))
        # all packages are processed
        yield self.env.all_of(events_processes)
        return truck

    def run(self):
        while True:
            # 开关机的事件控制
            yield self.env.process(self.check_switch())

            # filter out the match truck(LL/LA/AL/AA)11
            truck = yield self.trucks_q.get(lambda x: x.truck_type in self.truck_types)
            # truck start
            truck.insert_data(
                TruckRecordDict(
                    equipment_id=self.equipment_id,
                    time_stamp=self.env.now,
                    action="start", ))
            # 等待货车处理完
            truck = yield self.env.process(self.process_truck(truck))
            # truck end
            truck.insert_data(
                TruckRecordDict(
                    equipment_id=self.equipment_id,
                    time_stamp=self.env.now,
                    action="end", ))
            # truck is out
            self.done_trucks_q.put(truck)
            # vehicle turnaround time
            yield self.env.timeout(self.vehicle_turnaround_time)




