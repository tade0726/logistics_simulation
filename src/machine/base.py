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

        # 设备开启状态
        self.close = False