# -*- coding: utf-8 -*-


from src.machine.cross.test.config import Config
from src.vehicles import Pipeline
from src.machine.cross.test.logic_test import LogicTest
from simpy import Environment
from src.machine.cross import Cross


class CrossSimConfig(Config):
    # RANDOM_SEED = 57
    NUM_PACKAGES = 10
    #
    INTERVAL_TIME = 0

    TYPE_PIP_LINE = Pipeline
    # ==========================测试机配置参数===================================
    # 本次杭州仿真模为一个入口队列一个机器
    # 测试机器ID列表
    ID_TEST_MACHINE = ['test1']
    # 测试机资源字典
    TEST_MACHINE_RESOURCE_DIC = {'test1': {'resource': 0,
                                           'process_time': 0},
                                 'test2': {'resource': 0,
                                           'process_time': 0}}
    # 测试机器出端口id列表
    ID_NEXT_MACHINE = ['next_1']
    # 测试机器资源
    TEST_MACHINE_RESOURCE = 0  # 如果测试机器内部无资源调用，设置为0，否则设置资源数(如人力)
    # 测试机单资源处理时延
    PROCESS_TIME = None  # 如果测试机器没有处理货物延时，设置为None，否则设置为对应延时














if __name__ == '__main__':
    env = Environment()
    t1 = LogicTest(env, CrossSimConfig)
    t1.generator()
    env.process(t1.packages_generator())
    for tid in t1.config.ID_TEST_MACHINE:
        input_pip_line = t1.get_input_pip_line(tid)
        Cross(env=env,
              machine_id=tid,
              equipment_id=tid,
              input_pip_line=input_pip_line,
              pipelines_dict=t1.pipline,
              resource_dict=t1.resource_dict,
              equipment_resource_dict=t1.equipment_resource_dict)

    env.run(until=100)
