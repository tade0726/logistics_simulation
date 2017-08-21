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
        self.switch_res = simpy.PriorityResource(self.env, capacity=1)

    def check_switch(self):
        """开关机的事件控制"""
        t1 = self.env.now
        with self.switch_res.request() as req:
            yield req
        t2 = self.env.now
        LOG.logger_font.debug(f"sim time: {self.env.now} - machine: {self.equipment_id} - "
                              f"do something - t1: {t1} - t2: {t2}")