# -*- coding: utf-8 -*-

"""
作者：
日期：
说明：

交汇线的 class

"""


import simpy


class Cross(object):
    """
    Cross obj:
    sim one machine that have tow input ports and one out put port.
                  _ _ _ _ _ _ _
                 |             |
      input1 - ->|             |
                 |     x       |- ->output
      input2 - ->|             |
                 |_ _ _ _ _ _ _|

    """
    def __init__(self, env, input_x1, input_x2):
        """
        init class self args:
        Args:
            env: A simpy.Environment instance.
            input_x1: A simpy.PriorityStore which was put from ahead machine.
            input_x2: The same as input_x1.

        """
    pass