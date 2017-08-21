# -*- coding: utf-8 -*-

"""
Base machine for closing
"""

import simpy
from src.config import LOG


__all__ = ["BaseMachine"]


class BaseMachine:

    def __init__(self, env: simpy.Environment):
        self.env = env
        self.switch_res = simpy.PriorityResource(self.env)

    def _set_off_process(self, start, end):
        """进程占用开关资源，模拟关机状态

        start： 关机时间
        end： 开机时间

        """
        yield self.env.timeout(start)
        LOG.logger_font.debug(f"sim time: {self.env.now} - set off, until: {end}")
        with self.switch_res.request(priority=-1) as req:
            yield req
            yield self.env.timeout(end - start)

    def set_off(self, start, end):
        """API"""
        self.env.process(self._set_off_process(start, end))

    def check_switch(self):
        """开关机的事件控制"""
        t1 = self.env.now
        with self.switch_res.request() as req:
            yield req
        t2 = self.env.now
        LOG.logger_font.debug(f"sim time: {self.env.now} - machine: {self.equipment_id} - "
                              f"do something - t1: {t1} - t2: {t2}")