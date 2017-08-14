# -*- coding: utf-8 -*-

import simpy


class Machine:

    def __init__(self, env, resource_dict, machine_id, store):
        self.env = env
        self.resource_dict = resource_dict
        self.machine_id = machine_id
        self.resource = self.resource_dict[self.machine_id]
        self.store = store

    def do_something(self, item):
        with self.resource.request() as req:
            yield req
            yield self.env.timeout(1)
            print(f"{self.env.now} - process: {self.machine_id} - deal with item: {item}")

    def run(self):
        while True:
            item = yield self.store.get()
            self.env.process(self.do_something(item))
            yield env.timeout(3)


def change_resource_limit(env, resource_dict, time):
    yield env.timeout(time)
    for resource in resource_dict.values():
        resource._capacity = 4


if __name__ == '__main__':

    env = simpy.Environment()
    store = simpy.Store(env)
    store.items = [f'item_{i}' for i in range(10000)]

    resource_dict = {}

    for i in range(6):
        resource_dict[i] = simpy.Resource(env, capacity=1)

    machines = [ Machine(env, resource_dict, i, store) for i in range(6)]
    env.process(change_resource_limit(env, resource_dict, 10))
    for machine in machines:
        env.process(machine.run())

    env.run()


