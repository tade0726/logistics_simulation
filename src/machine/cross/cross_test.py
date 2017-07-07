# -*- coding: utf-8 -*-

"""
作者：kissf lu
日期：2017/7/7
说明：杭州项目，汇流点类模块 仿真测试

"""

from simpy import Environment
from simpy import PriorityStore
from simpy import PriorityItem
from src.machine.cross import Cross
import random as rd


RANDOM_SEED = 42


def generator_packages_queue():
    """
    """
    env = Environment()
    input_queue_dic = {
        'x1_in1': PriorityStore(env)
        , 'x1_in2': PriorityStore(env)
                       }

    #  for k, v in input_queue_dic.items():

    #  cross_test(env, input_queue_dic)


def cross_test():
    """
    cross module test: Cross 模块测试单元
    """
    env = Environment()
    input_queue_dic = generator_packages_queue()
    output_queue = PriorityStore(env)
    cross = Cross(env=env, id_x='x1', input_dic=input_queue_dic, out_put=output_queue)
    env.run()


if __name__ == '__main__':
    print('run!')
    generator_packages_queue()
