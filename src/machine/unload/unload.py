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
import random

from src.controllers import PathGenerator

TRUCK_CONVERT_TIME = 300


class Unload:

    def __init__(self,
                 env: simpy.Environment,
                 machine_id: str,
                 equipment_id: str,
                 unload_setting_dict: dict,
                 reload_setting_dict: dict,
                 trucks_q: simpy.FilterStore,
                 pipelines_dict: defaultdict,
                 resource_dict: defaultdict,
                 equipment_resource_dict:dict,
                 path_generator: PathGenerator,
                 ):

        self.env = env
        self.machine_id = machine_id
        self.equipment_id = equipment_id # pipeline id last value, for other machines
        self.truck_types = unload_setting_dict[equipment_id]
        self.reload_setting_dict = reload_setting_dict
        self.trucks_q = trucks_q
        self.pipelines_dict = pipelines_dict

        self.resource_id = equipment_resource_dict[equipment_id]
        self.resource = resource_dict[self.resource_id]['resource']
        self.process_time = resource_dict[self.resource_id]['process_time']

        self.num_of_truck = 0
        self.packages_processed = dict()
        self.done_trucks = simpy.Store(env)

        # store data
        self.package_records = []
        self.truck_records = []

        # path generator
        self.path_generator = path_generator.path_generator

    def process_package(self, process_idx, package: Package):

        with self.resource.request() as req:
            yield req
            next_pipeline = package.next_pipeline

            package.start_serve()
            yield self.env.timeout(self.process_time)
            package.end_serve()
            self.pipelines_dict[next_pipeline].put(package)
            self.packages_processed[process_idx].succeed()
            self.package_records.append(package.package_record)

    def run(self):

        while True:
            # filter out the match truck(LL/LA/AL/AA)
            truck = yield self.trucks_q.get(lambda x: x.truck_type in self.truck_types)

            print(f"truck {truck.item_id} start process at {self.env.now}")

            # add data
            truck.start_serve()
            truck.add_machine_id(machine_id=self.machine_id)

            # init packages_processed empty
            self.packages_processed = dict()

            for process_idx, package_record in truck.store.iterrows():

                package_start = self.machine_id
                # building key
                dest_code = package_record["dest_zone_code"]
                dest_type = package_record["dest_type"]
                parcel_type = package_record["parcel_type"]
                sorter_type = "reload" if parcel_type == "parcel" else "small_sort"

                try:
                    plan_path = self.path_generator(package_start, dest_code, sorter_type, dest_type)
                except Exception as exc:
                    print(exc)
                    break # jump out of the loop

                # init package
                package = Package(env=self.env,
                                  item_id=package_record["parcel_id"],
                                  attr=package_record,
                                  path=plan_path,
                                  )
                print(f"package {package.item_id} unloaded..")
                # package add data
                package.start_wait()
                # pop and mark
                package.pop_mark(is_first=True)
                # need request resource for processing
                self.packages_processed[process_idx] = self.env.event()
                self.env.process(self.process_package(process_idx, package))

            # all the package are processed
            yield self.env.all_of(self.packages_processed.values())
            # truck add data
            truck.end_serve()
            self.truck_records.append(truck.truck_record)
            # truck is out
            self.done_trucks.put(truck)
            # truck convert time
            yield self.env.timeout(TRUCK_CONVERT_TIME)
            self.num_of_truck += 1




