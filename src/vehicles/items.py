# -*- coding: utf-8 -*-

"""
作者：
日期：
说明：

包裹 class
货物 class
Uld class

"""
import simpy

__all__ = ["Package", "Truck", "Uld"]


class Package:

    def __init__(self, attr, now_position: str=None, next_position: str=None):
        """
        :param attr: package records
        :param now_position: position of last machine(pipeline)
        :param next_position: position of next machine(pipeline)
        """
        # using for pipeline length calculations
        self.now_position = now_position
        self.next_position = next_position

        self.attr = attr

        # record of the path of the package,
        # element will be a dict {'now_position': 'some where', 'next_position', 'some where', 'last_timestamp': 1000}
        # for record
        self.path = ()
        # for popping
        self.plan_path = []
        # for time
        self.time_records = []

    def __str__(self):
        """
        :return:
        """
        display_dct = dict(self.attr)

        return f"<package attr:{dict(display_dct)}>"

# vehicles


class Truck:

    def __init__(self, truck_id, come_time, packages:pd.DataFrame):
        """
        :param truck_id: self explain
        :param come_time: self explain
        :param packages: a dataframe contain all packages
        """
        self.truck_id = truck_id
        self.come_time = come_time
        self.store = packages

    def __str__(self):
        """
        :return:
        """
        return f"<truck_id: {self.truck_id}, come_time: {self.come_time}, store_size:{len(self.store)}>"


class Uld:
    pass


class Pipeline:

    """传送带"""

    def __init__(self,
                 env: simpy.Environment,
                 delay_time: float,
                 last_pipeline_id: str,
                 next_pipline_id: str,
                 queue_id: str,
                 ):

        self.env = env
        self.delay = delay_time
        self.queue = simpy.PriorityStore(env)

        # self.last_pipeline_id = last_pipeline_id
        # self.next_pipline_id = next_pipline_id

        self.pipeline_id = (last_pipeline_id, next_pipline_id)
        self.queue_id = queue_id
        self.package_counts = 0
        self.package_counts_time = []
        # 加入计数器
        self.env.process(self.get_counts())

    def get_counts(self):
        """计数器"""
        while True:
            self.env.timeout(1)
            self.package_counts_time.append((self.env.now, self.package_counts))

    def latency(self, item: Package):
        """模拟传送时间"""
        yield self.env.timeout(self.delay)
        self.queue.put(simpy.PriorityItem(priority=self.env.now,
                                          item=item))

    def put(self, item: Package):
        self.package_counts += 1
        self.env.process(self.latency(item))

    def get(self):
        self.package_counts -= 1
        return self.queue.get()