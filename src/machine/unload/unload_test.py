import simpy
import pickle
from os.path import join

from src.vehicles import Pipeline, Package
from src.db import SaveConfig

# fixme
class Truck:

    def __init__(self, truck_id, env: simpy.Environment):
        self.env = env
        self.truck_id = truck_id
        self.packages = [Package(env, item_id=f"{truck_id}_package_{i}") for i in range(30)]
        self.truck_record = \
            dict(truck_id=truck_id)

    def start_wait(self):
        self.truck_record["start_wait"] = self.env.now

    def start_serve(self):
        self.truck_record["start_serve"] = self.env.now

    def end_serve(self):
        self.truck_record["end_serve"] = self.env.now


def truck_controllers(env: simpy.Environment, truck_q: simpy.Store):

    for i in range(100):
        truck = Truck(truck_id=f"truck_{i}", env=env)
        truck.start_wait()
        truck_q.put(truck)
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
        self.package_records = []
        self.truck_records = []

    def processing(self, idx, package):

        with self.resource.request() as req:
            yield req

            package.start_serve()
            yield self.env.timeout(self.process_time)
            package.end_serve()
            # add data
            self.package_records.append(package.package_record)
            self.next_q.put(package)
            self.packages_processed[idx].succeed()

    def run(self):
        while True:

            truck = yield self.truck_q.get()
            truck.start_serve()

            for idx, package in enumerate(truck.packages):

                package.start_wait()
                self.packages_processed[idx] = self.env.event()
                self.env.process(self.processing(idx, package))

            yield self.env.all_of(self.packages_processed.values())
            # truck convert time
            truck.end_serve()
            self.truck_records.append(truck.truck_record)
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
    truck_records = []
    package_records = []

    for machine in unload_machines:
        truck_records.extend(machine.truck_records)
        package_records.extend(machine.package_records)

    pipeline_on_con_records = next_q.latency_counts_time
    pipeline_on_wait_records = next_q.machine_waiting_counts_time

    with open(join(SaveConfig.DATA_DIR, "truck_records.list"), "wb") as file:
        pickle.dump(truck_records, file)

    with open(join(SaveConfig.DATA_DIR, "package_records.list"), "wb") as file:
        pickle.dump(package_records, file)

    with open(join(SaveConfig.DATA_DIR, "pipeline_on_con_records.list"), "wb") as file:
        pickle.dump(pipeline_on_con_records, file)

    with open(join(SaveConfig.DATA_DIR, "pipeline_on_wait_records.list"), "wb") as file:
        pickle.dump(pipeline_on_wait_records, file)


