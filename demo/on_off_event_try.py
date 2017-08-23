import simpy

class Unload:

    def __init__(self, env: simpy.Environment):

        self.env = env
        self.store = simpy.Store(env)
        self.store_end = simpy.Store(env)
        self.env.process(self.run())
        self.env.process(self.put_item())

        self.close_time = [3, 10]
        self.open_time = [7, 15]

    def put_item(self):
        for i in range(20):
            item = f"item_{i}"
            yield self.env.timeout(1)
            self.store.put(item)
            # print(f"{self.env.now}: gen {item}")

    def run(self):
        while True:

            item = yield self.store.get()

            if self.env.now >= self.close_time[0]:

                self.close_time.pop(0)
                self.store.put(item)
                print(f"{self.env.now}: put back {item}")
                open_time = self.open_time.pop(0)

                print(f"{self.env.now}: machine close")
                duration_time = open_time - self.env.now
                print(f"{self.env.now}: machine reopen at {open_time}")
                yield self.env.timeout(duration_time)
                print(f"{self.env.now}: machine reopen")

                continue

            print(f"{self.env.now}: get {item}")
            print(f"{self.env.now}: process {item}")

            self.store_end.put(item)







env = simpy.Environment()
unload = Unload(env)
env.run()

print(unload.store.items)
print(unload.store_end.items)


