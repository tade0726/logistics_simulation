# -*- coding: utf-8 -*-


"""
Author : Ted
Date: 2017-08-29
Demo of how to combine filter store and priority store

"""

import simpy
from simpy import PriorityItem, PriorityStore, FilterStore
import random


class Item:

    def __init__(self, item_type, i, j, p):
        self.item_type = item_type
        self.i = i  # generate at time i
        self.j = j  # number j items in i seconds
        self.p = p  # priority

    def __str__(self):
        return f"item_{self.i}_{self.j}_p{self.p} - item_type: {self.item_type}"


def generate_item(env):

    for i in range(20):
        for j in range(10):
            p = random.randint(0, 3000)
            i_type = random.choice(['a', 'b',])
            item = Item(i_type, i, j, p)
            priority_store.put(PriorityItem(p, item))

        yield env.timeout(1)


def priority_put(env, in_q, out_q):
    while True:
        priority_item = yield in_q.get()
        item = priority_item.item
        # print(f"{env.now}: +put {item}")
        out_q.put(item)


def filter_get(env, out_q, item_type: str='a'):
    while True:
        item = yield out_q.get(lambda x: x.item_type == item_type)
        print(f"{env.now}: -get {item}")
        # yield env.timeout(1)


if __name__ == '__main__':

    env = simpy.Environment()

    filter_store = FilterStore(env)
    priority_store = PriorityStore(env)

    env.process(generate_item(env))
    env.process(priority_put(env, in_q=priority_store, out_q=filter_store))
    env.process(filter_get(env, out_q=filter_store, item_type='a'))
    # env.process(filter_get(env, out_q=filter_store, item_type='b'))
    # env.process(filter_get(env, out_q=filter_store, item_type='c'))

    env.run()
