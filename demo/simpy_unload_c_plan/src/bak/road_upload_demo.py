# -*- coding: utf-8 -*-

"""
author:  Ted
date: 2017-06-12
des: demo road upload

"""

import itertools
import random
import simpy


# some init parameters

UNLOAD_EFFICIENCY = 3600.0 / 1000  ##卸货效率
SPEED = 1  # 传送带速度（单位：米/秒）
NC_SPEED = 2
IR_SPEED = 2
DRIVE = 5 * 60  ##货车转换时间



