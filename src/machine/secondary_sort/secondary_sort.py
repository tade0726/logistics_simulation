import simpy


class SecondarySort:
    def __init__(self, env, machine_id, queue, logger):
        self.env = env
        self.machine_id = machine_id
        self.queue = queue

        self.i_infeed = queue #todo @lanyi: infeed io
        self.i_outlet = queue #todo @lanyi: outlet io

        self.c_infeed = queue #todo @lanyi: infeed io
        self.c_outlet = queue #todo @lanyi: outlet io

        self.shortcut_time = queue #todo @lanyi: shortcut time
        self.machine_time = queue #todo @lanyi: machine time

        self.log_error = logger(log_name=f"error_{self.machine_id}")

    def shortcut(self):
        while True:
            yield self.env.timeout(self.shortcut_time)

    def machine(self):
        while True:
            yield self.env.timeout(self.machine_time)

    def run(self):
        while True:
            # todo @lanyi: get destination attr
            package = yield self.queue.get()
            package = package.item
            if package.attr['type'] == "half":
                self.env.process(self.shortcut())
            self.env.process(self.machine())
