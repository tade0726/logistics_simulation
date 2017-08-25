import simpy


def get_item(i, env, store):

    while True:
        item = yield store.get()
        print(f"{env.now} - process_{i} get item {item}")
        yield env.timeout(i)



def put_item(env, store):
    for i in range(10):
        item = f"item_{i}"
        store.put(item)


env = simpy.Environment()
store = simpy.Store(env)


put_item(env, store)

for i in range(1, 4):
    env.process(get_item(i, env, store))

env.run()
