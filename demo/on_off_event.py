import simpy

class Unload:

    def __init__(self, env: simpy.Environment):

        self.env = env
        self.machine_switch = self.env.event()
        self.machine_switch.succeed()


    def set_on(self):
        self.machine_switch.succeed()

    def set_off(self):
        self.machine_switch = self.env.event()

    def run(self):
        while True:

            t1 = self.env.now
            yield self.machine_switch
            t2 = self.env.now
            print(f"{self.env.now} - do some thing - t1: {t1} - t2: {t2}")

            yield self.env.timeout(1)

            if self.env.now >= 100:
                self.env.exit()


class Controller:

    def __init__(self, env: simpy.Environment):
        self.env = env

    def change(self, machine, on_off, time):

        if time:
            yield self.env.timeout(time)

        if on_off:
            machine.set_on()
            print(f"{self.env.now} - open machine")
        else:
            machine.set_off()
            print(f"{self.env.now} - close machine")

        yield self.env.timeout(0)

    def control(self, machine):

        for time in range(0, 100, 10):
            if time % 20:
                self.env.process(self.change(machine, True, time))
            else:
                self.env.process(self.change(machine, False, time))

if __name__ == '__main__':
    env = simpy.Environment()
    controller = Controller(env)
    machine = Unload(env)

    controller.control(machine)
    env.process(machine.run(), )

    env.run()

