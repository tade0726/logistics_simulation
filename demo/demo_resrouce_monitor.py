import simpy
from collections import namedtuple


ResourceRecords = namedtuple("ResourceRecord", ['process_name', 'resource_id', 'time_stamp', 'wait_numbers'])


class MonitoredPriorityResource(simpy.PriorityResource):

    def __init__(self, data: list, resource_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
        self.resource_id = resource_id

    def request(self, *args, **kwargs):
        name = kwargs.pop('name')
        record = ResourceRecords(process_name=name,
                                 resource_id=self.resource_id,
                                 time_stamp=self._env.now,
                                 wait_numbers=len(self.queue),)
        self.data.append(record)
        return super().request(*args, **kwargs)

    def release(self, *args, **kwargs):
        return super().release(*args, **kwargs)


def process_thing(env):
    name = "p1"
    for _ in range(100):
        with res.request(name=name) as req:
            yield req
            yield env.timeout(1)


def process_thing2(env):
    name = "p2"
    for _ in range(10):
        with res.request(name=name, priority=-1) as req:
            yield req
            yield env.timeout(5)
        yield env.timeout(10)


env = simpy.Environment()
data = list()

res = MonitoredPriorityResource(data, "test1", env=env, capacity=1)
env.process(process_thing(env))
env.process(process_thing2(env))

env.run()

for line in data:
    print(line)