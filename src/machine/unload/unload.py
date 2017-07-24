# -*- coding: utf-8 -*-


"""
author: Ted
date: 2017-07-11
des:

unload modules
"""
import simpy
from collections import defaultdict
from src.vehicles import Package
from src.utils import TruckRecord, PackageRecord

import logging

# todo: using data from get_parameters
TRUCK_CONVERT_TIME = 90


class Unload:

    def __init__(self,
                 env: simpy.Environment,
                 machine_id: str,
                 unload_setting_dict: dict,
                 reload_setting_dict: dict,
                 trucks_q: simpy.FilterStore,
                 pipelines_dict: dict,
                 resource_dict: defaultdict,
                 equipment_resource_dict: dict,
                 ):

        self.env = env
        self.machine_id = machine_id
        self.unload_setting_dict = unload_setting_dict
        self.reload_setting_dict = reload_setting_dict
        self.trucks_q = trucks_q
        self.pipelines_dict = pipelines_dict
        self.resource_dict = resource_dict
        self.equipment_resource_dict = equipment_resource_dict

        self.num_of_truck = 0
        self.packages_processed = dict()
        self.done_trucks = simpy.Store(env)
        # data store
        self.truck_records = []
        self.package_records = []

        self.resource_set = self._set_machine_resource()

    def _set_machine_resource(self):
        """"""
        if self.equipment_resource_dict:
            self.equipment_id = self.machine_id   # pipeline id last value, for other machines
            self.resource_id = self.equipment_resource_dict[self.equipment_id]
            self.resource = self.resource_dict[self.resource_id]['resource']
            self.process_time = self.resource_dict[self.resource_id]['process_time']
            self.truck_types = self.unload_setting_dict[self.equipment_id]

        else:
            raise RuntimeError('cross machine',
                               self.machine_id,
                               'not initial equipment_resource_dict!')

    def process_package(self, process_idx, package: Package):

        with self.resource.request() as req:
            yield req

            package.insert_data(
                PackageRecord(
                    equipment_id=self.equipment_id,
                    package_id=package.item_id,
                    time_stamp=self.env.now,
                    action="start",))

            yield self.env.timeout(self.process_time)

            package.insert_data(
                PackageRecord(
                    equipment_id=self.equipment_id,
                    package_id=package.item_id,
                    time_stamp=self.env.now,
                    action="end",))

            # error package store in
            try:
                package.set_path(package_start=self.machine_id)
                self.pipelines_dict[package.next_pipeline].put(package)
            except Exception as exc:
                msg = f"error: {exc}, package: {package}"
                logging.error(msg)
                self.pipelines_dict["unload_error_packages"].put(package)

            self.packages_processed[process_idx].succeed()

    def run(self):

        while True:
            # filter out the match truck(LL/LA/AL/AA)
            truck = yield self.trucks_q.get(lambda x: x.truck_type in self.truck_types)

            truck.insert_data(
                TruckRecord(
                    equipment_id=self.equipment_id,
                    truck_id=truck.item_id,
                    time_stamp=self.env.now,
                    action="start",
                    store_size=truck.store_size))

            # init packages_processed empty
            self.packages_processed = dict()

            for process_idx, package in enumerate(truck.store):

                # add package wait data
                package.insert_data(
                    PackageRecord(
                        equipment_id=self.equipment_id,
                        package_id=package.item_id,
                        time_stamp=truck.come_time,
                        action="wait", ))

                # need request resource for processing
                self.packages_processed[process_idx] = self.env.event()
                self.env.process(self.process_package(process_idx, package))

            # all the package are processed
            yield self.env.all_of(self.packages_processed.values())

            # insert data
            truck.insert_data(
                TruckRecord(
                    equipment_id=self.equipment_id,
                    truck_id=truck.item_id,
                    time_stamp=self.env.now,
                    action="end",
                    store_size=truck.store_size))

            # truck is out
            self.done_trucks.put(truck)
            # truck convert time
            yield self.env.timeout(TRUCK_CONVERT_TIME)




