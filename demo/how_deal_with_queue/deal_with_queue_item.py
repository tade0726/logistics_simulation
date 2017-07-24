# -*- coding: utf-8 -*-

"""
Date: 2017-07-05
Author: Ted

Des:
 Try to deal with the problem of moving object


"""
import simpy


# config
PROCESS_TIME = 12
CON_BELT_TIME = 3


def con_belt_process(env, con_belt_time, package, next_q):

    while True:
        print(f"item: {package} start move at {env.now}")
        yield env.timeout(con_belt_time)
        next_q.put(simpy.PriorityItem(priority=env.now, item=package))
        print(f"item: {package} end move at {env.now}")
        env.exit()


def machine(env: simpy.Environment(),
            last_q: simpy.PriorityStore,
            next_q: simpy.PriorityStore,
            machine_id: str):

    while True:
        package = yield last_q.get()
        item = package.item
        yield env.timeout(PROCESS_TIME)
        env.process(con_belt_process(env, CON_BELT_TIME, item, next_q))
        print(f'Time at {env.now}, machine: {machine_id}, done item {machine_id}')


if __name__ == '__main__':

    env = simpy.Environment()

    last_q = simpy.PriorityStore(env)
    next_q = simpy.PriorityStore(env)

    for i in range(100):
        last_q.put(simpy.PriorityItem(priority=1, item=f'item_{i}'))

    for i in range(5):
        env.process(machine(env, last_q, next_q, machine_id=f'm_{i}'))
    env.run()

