import simpy

class Unload:

    def __init__(self, env: simpy.Environment):

        self.env = env
        self.truck = simpy.Store(env)

        self.switch_res = self.env.event()
        self.switch_res.succeed()

    def set_off(self, start):
        yield self.env.timeout(start)
        self.switch_res = self.env.event()
        print(f"{self.env.now} - close")

    def set_on(self, start):
        yield self.env.timeout(start)

        try:
            self.switch_res.succeed()
            print(f"{self.env.now} - open")
        except RuntimeError as exc:
            print(f"{self.env.now} - already open")

    def run(self):
        while True:
            item = yield self.truck.get()
            t1 = self.env.now
            yield self.switch_res
            t2 = self.env.now
            print(f"{self.env.now} - do some thing - t1: {t1} - t2: {t2} - item: {item}")


class Controller:

    def __init__(self, env: simpy.Environment):
        self.env = env

    def control(self, machine):

        for time in range(0, 100, 10):
            if time % 20:
                self.env.process(machine.set_off(start=time,))
            else:
                self.env.process(machine.set_on(start=time,))


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

