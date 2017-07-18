import simpy
import random
from collections import defaultdict
import pickle
from os.path import join

from src.vehicles import Pipeline
from src.db import SaveConfig


class Truck:

    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = [f"truck_{truck_id}_package_{i}" for i in range(30)]


def truck_controllers(env: simpy.Environment, truck_q: simpy.Store):
    for i in range(100):
        truck_q.put(Truck(truck_id=f"truck_{i}"))
        wait_time = 5
        yield env.timeout(wait_time)


class Unload:

    def __init__(self, env: simpy.Environment, machine_id: str, truck_q: simpy.Store, next_q: Pipeline):

        self.env = env
        self.machine_id = machine_id
        self.truck_q = truck_q
        self.next_q = next_q
        self.truck_counts = 0
        self.truck_convert_time = 300
        self.resource = simpy.Resource(env=self.env, capacity=2)
        self.packages_processed = dict()
        self.process_time = 3.6

        # store data
        self.package_records = defaultdict(dict)
        self.truck_records = defaultdict(dict)

    def processing(self, idx, package):

        with self.resource.request() as req:
            yield req

            print(f"{package} start processing unload_{self.machine_id} at {self.env.now}")
            self.package_records[package]["start_process"] = self.env.now

            yield self.env.timeout(self.process_time)

            print(f"{package} end processing unload_{self.machine_id} at {self.env.now}")
            self.package_records[package]["end_process"] = self.env.now
            self.package_records[package]["machine_id"] = self.machine_id
            self.package_records[package]["package_id"] = package

            self.next_q.put(package)
            self.packages_processed[idx].succeed()

    def run(self):
        while True:

            truck = yield self.truck_q.get()
            truck_arrive_time = self.env.now

            print(f"truck_{truck.truck_id} enter unload_{self.machine_id} at {truck_arrive_time}")
            self.truck_records[truck.truck_id]["enter_machine"] = truck_arrive_time

            for idx, package in enumerate(truck.packages):
                print(f"{package} start waiting unload_{self.machine_id} at {truck_arrive_time}")
                self.package_records[package]["start_wait"] = truck_arrive_time

                self.packages_processed[idx] = self.env.event()
                self.env.process(self.processing(idx, package))

            yield self.env.all_of(self.packages_processed.values())
            # truck convert time
            print(f"truck_{truck.truck_id} leave unload_{self.machine_id} at {self.env.now}")
            self.truck_records[truck.truck_id]["leave_machine"] = self.env.now
            self.truck_records[truck.truck_id]["machine_id"] = self.machine_id
            self.truck_records[truck.truck_id]["truck_id"] = truck.truck_id

            yield self.env.timeout(self.truck_convert_time)
            self.truck_counts += 1


if __name__ == "__main__":

    env = simpy.Environment()
    truck_q = simpy.Store(env)
    next_q = Pipeline(env, delay_time=5, )

    unload_machines = [Unload(env, f"unload_{i}", truck_q, next_q) for i in range(2)]

    for machine in unload_machines:
        env.process(machine.run())

    env.process(truck_controllers(env, truck_q))
    env.run()

    # loading data
    truck_records = dict()
    package_records = dict()

    for machine in unload_machines:
        truck_records.update(machine.truck_records)
        package_records.update(machine.package_records)

    pipeline_on_con_records = next_q.latency_counts_time
    pipeline_on_wait_records = next_q.machine_waiting_counts_time

    with open(join(SaveConfig.DATA_DIR, "truck_records.dict"), "wb") as file:
        pickle.dump(truck_records, file)

    with open(join(SaveConfig.DATA_DIR, "package_records.dict"), "wb") as file:
        pickle.dump(package_records, file)

    with open(join(SaveConfig.DATA_DIR, "pipeline_on_con_records.list"), "wb") as file:
        pickle.dump(pipeline_on_con_records, file)

    with open(join(SaveConfig.DATA_DIR, "pipeline_on_wait_records.list"), "wb") as file:
        pickle.dump(pipeline_on_wait_records, file)
