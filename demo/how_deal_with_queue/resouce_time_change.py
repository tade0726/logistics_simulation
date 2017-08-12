# -*- coding: utf-8 -*-


"""
Author: Ted

testing changing resource
"""

import simpy


env = simpy.Environment()
store = simpy.Store(env)

store.items = [f'item_{i}' for i in range(100)]
resource_dict = {}

for i in range(6):
    resource_dict[i] = simpy.Resource(env, capacity=1)

resource = resource_dict[4]

def do_something(env, resource, process_num):
    while True:
        if len(store.items) < 50:
            resource._capacity = 3
        with resource.request() as req:
            yield req
            item = yield store.get()
            yield env.timeout(1)
            print(f"{env.now} - process: {process_num} - deal with item: {item}")

for process_num in range(3):
    env.process(do_something(env, resource, process_num))
env.run()
