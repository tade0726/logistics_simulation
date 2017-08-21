import simpy

class Unload:

    def __init__(self, env: simpy.Environment):

        self.env = env
        self.truck = simpy.Store(env)

        self.switch_res = simpy.PriorityResource(self.env)

    def set_off(self, start, end):
        yield self.env.timeout(start)
        print(f"{self.env.now} - set off, until: {end}")
        with self.switch_res.request(priority=-1) as req:
            yield req
            yield self.env.timeout(end - start)

    def check(self):
        t1 = self.env.now
        with self.switch_res.request() as req:
            yield req
        t2 = self.env.now
        return t1, t2

    def run(self):
        while True:
            t1, t2 = yield self.env.process(self.check())
            item = yield self.truck.get()
            print(f"{self.env.now} - do some thing - t1: {t1} - t2: {t2} - item: {item}")


class Controller:

    def __init__(self, env: simpy.Environment):
        self.env = env

    def control(self, machine):

        for time in range(0, 100, 10):
            if time % 20:
                self.env.process(machine.set_off(start=time, end=time+10))


def truck_come(truck, env, delay):
    yield env.timeout(delay)
    truck.put(f"t_{delay}")

if __name__ == '__main__':
    env = simpy.Environment()
    controller = Controller(env)
    machine = Unload(env)

    controller.control(machine)

    env.process(machine.run(), )

    for t in range(10, 100, 2):
        env.process(truck_come(machine.truck, env, t))

    env.run()

