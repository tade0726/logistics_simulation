# -*- coding: utf-8 -*-

"""
======================================================================================================
                                                     杭州HUB仿真项目

                                    项目启动日期：2017年7月6日
                                    项目启动标识：AIRPORT OF EZHOU'S PROJECT  -- HZ
                                    ===========================================
                                    代码创建日期：2017年7月6日
                                    代码创建工程师：卢健
                                    代码版本：1.0
                                    版本更新日期：2017年7月6日
                                    版本更新工程师：卢健

                                    代码整体功能描述：汇流点机器测试单元
                                                      1、用于测试cross类模块；


=====================================================================================================
"""

from simpy import Environment
from simpy import PriorityStore
from simpy import PriorityItem
from simpy import Resource
from src.machine.cross import Cross
import random as rd
from numpy.random import choice


RANDOM_SEED = 42
NUM_PORT_ABLE = 2
NUM_PACKAGES = 10
QUEUE_GENERATOR_GAP = 10
INPUT_QUEUE_ID = ['x1_in1', 'x1_in2']
INPUT_QUEUE_DIC = {}
OUTPUT_QUEUE = None
CROSS_ID = 'x1'
NUM_RUN_TIME = 5
rd.seed(RANDOM_SEED)


def machine_package(env, generator_queue_res):
    """"""
    num = 0
    while True:
        env.process(machine_queue_input(env, generator_queue_res, num))
        num += 1
        yield env.timeout(1)


def machine_queue_input(env, generator_queue_res, package_id):
    """"""
    print('package', package_id, 'come', 'at', env.now)
    with generator_queue_res.request() as req:
        yield req
        id_queue = str(choice(INPUT_QUEUE_ID))
        id_package = ''.join([id_queue, '_', str(package_id)])
        package_items = {'package_id': id_package, 'package_gen_time': env.now}
        # print('put package', package_id, 'into queue', id_queue, 'at', env.now)
        yield INPUT_QUEUE_DIC[id_queue].put(PriorityItem(priority=env.now, item=package_items))
        # print('queue', id_queue,'info:', INPUT_QUEUE_DIC[id_queue].items) rd.randint(2, 30)
        # yield env.timeout(2)


def cross_sim():
    """
    cross module test: Cross 模块测试单元
    """
    env = Environment()
    INPUT_QUEUE_DIC.update({'x1_in1': PriorityStore(env=env), 'x1_in2': PriorityStore(env=env)})
    generator_queue_res = Resource(env=env, capacity=NUM_PORT_ABLE)
    env.process(machine_package(env=env, generator_queue_res=generator_queue_res))
    OUTPUT_QUEUE = PriorityStore(env)
    cross = Cross(env=env, id_x=CROSS_ID, input_dic=INPUT_QUEUE_DIC, out_put=OUTPUT_QUEUE)
    env.run(until=50)


if __name__ == '__main__':
    print('run!')
    cross_sim()
    print('end')
