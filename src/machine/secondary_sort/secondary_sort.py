class SecondarySort:
    def __init__(self, env, machine_id, queue, logger):
        self.env = env
        self.machine_id = machine_id
        self.queue = queue

        self.log_record = logger(log_name=f"record_{self.machine_id}")
        self.log_error = logger(log_name=f"error_{self.machine_id}")

    def shortcut(self):
        while True:
            self.env.timeout(1)
            pass


    def machine(self):
        while True:
            package = yield self.queue.get()
            package = package.item
            destination = package.attr['destination_port']

    def run(self):
        while True:
            package = yield self.queue.get()
            package = package.item
            if package.attr['type'] == "half":
                self.shortcut()
            else:
                pass