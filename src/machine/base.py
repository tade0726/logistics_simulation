# -*- coding: utf-8 -*-

"""
Base machine for closing
"""

import simpy


__all__ = ["BaseMachine"]


class BaseMachine:

    def __init__(self, env: simpy.Environment):
        self.env = env
        self.switch_res = simpy.PriorityResource(self.env)

    def set_off(self, start, end):
        """进程占用开关资源，模拟关机状态

        start： 关机时间
        end： 开机时间

        """
        yield self.env.timeout(start)
        print(f"{self.env.now} - set off, until: {end}")
        with self.switch_res.request(priority=-1) as req:
            yield req
            yield self.env.timeout(end - start)