import simpy
# todo @lanyi: in & out queues


class Secondary(object):
    def __init__(self, env, queue):
        self.env = env
        self.queue = queue

    def run(self, cart: simpy.Resource):
        while True:
            with cart.request():
                package = yield self.queue.get()


