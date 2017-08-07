import simpy
import random
from src.config import Small_code


class Item:
    def __init__(self, idx, id=None):
        self.idx = idx
        self.id = id

    def __str__(self):
        return f"<item idx: {self.idx}, id: {self.id}>"


def put_item(env):
    for i in range(300):
        yield env.timeout(random.randint(1, 2))
        item = Item(idx=i)
        print(f"{env.now}: generated {item} ")
        store.put(item)


def get_numbers(env):
    while True:
        item = yield store.get()
        yield env.timeout(4)
        item.id = next(Small_code.code_generator)
        print(f"{env.now}: deal with {item}")
        done_store.put(item)


if __name__ == "__main__":
    env = simpy.Environment()
    store = simpy.Store(env)
    done_store = simpy.Store(env)

    env.process(put_item(env))
    for _ in range(4):
        env.process(get_numbers(env))

    env.run()