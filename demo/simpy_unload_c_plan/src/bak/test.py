import simpy


env = simpy.Environment()
store = simpy.Store(env=env)

for i in range(10):
    store.put(i)

def no_time(env):
    i = 0
    while True:
        i += 1
        item = yield store.get()
        print(f"no time spending at {env.now}, deal with {item}. loop: {i}")
        # yield env.timeout(1)

def one_time(env):
    while True:
        item = yield store.get()
        print(f"no time spending {env.now}, deal with {item}")
        yield env.timeout(1)

env.process(no_time(env))
# env.process(one_time(env))

env.run()