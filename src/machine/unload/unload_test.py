import simpy
import random


class Truck:

    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = [f"truck_{truck_id}_package_{i}" for i in range(30)]


def truck_controllers(env: simpy.Environment, truck_q: simpy.Store):
    for truck_id in range(100):
        truck_q.put(Truck(truck_id=truck_id))
        TIME = 5
        yield env.timeout(TIME)


class Unload:

    def __init__(self, env: simpy.Environment, machine_id: int, truck_q: simpy.Store, next_q: simpy.Store):

        self.env = env
        self.machine_id = machine_id
        self.truck_q = truck_q
        self.next_q = next_q
        self.truck_counts = 0
        self.truck_convert_time = 300
        self.resource = simpy.Resource(env=self.env, capacity=2)
        self.packages_processed = dict()
        self.process_time = 3.6

    def processing(self, idx, package):

        with self.resource.request() as req:
            yield req
            yield self.env.timeout(self.process_time)
            print(f"{package} start processing unload_{self.machine_id} at {self.env.now}")
            self.next_q.put(package)
            self.packages_processed[idx].succeed()

    def run(self):
        while True:

            truck = yield self.truck_q.get()

            for idx, package in enumerate(truck.packages):
                print(f"{package} enter unload_{self.machine_id} at {self.env.now}")
                self.packages_processed[idx] = self.env.event()
                self.env.process(self.processing(idx, package))

            yield self.env.all_of(self.packages_processed.values())
            # truck convert time
            yield self.env.timeout(self.truck_convert_time)
            self.truck_counts += 1


if __name__  == "__main__":

    env = simpy.Environment()
    truck_q = simpy.Store(env)
    next_q = simpy.Store(env)

    unload_machines = [ Unload(env, machine_id, truck_q, next_q) for machine_id in range(2)]

    for machine in unload_machines:
        env.process(machine.run())
    env.process(truck_controllers(env, truck_q))

    env.run()
