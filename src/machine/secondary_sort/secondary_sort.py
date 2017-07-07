import simpy


class SecondarySort:
    def __init__(self, env, machine_id, queue, logger):
        self.env = env
        self.machine_id = machine_id
        self.queue = queue

        self.log_error = logger(log_name=f"error_{self.machine_id}")

        self.wait_queue = simpy.PriorityStore(self.env)

    def machine(self, time):
        while True:
            yield self.env.timeout(time)

    def run(self):
        while True:
            package = yield self.wait_queue.get()
            package = package.item
            destination = package.attr['dest_code']
            process_time = package.attr['time']
            #todo @lanyi will be replaced with a function
            if destination in ['c1']:
                #todo @lanyi shortcut function
                pass
            self.env.process(self.machine(process_time))
