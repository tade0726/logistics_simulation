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
        self.switch_event = self.env.event()
        self.switch_event.succeed()

    def set_machine_open(self):
        self.switch_event.succeed()

    def set_machine_close(self):
        self.switch_event = self.env.event()

