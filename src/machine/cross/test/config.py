# -*- coding: utf-8 -*-


from simpy import Store


__all__ = ['Config']


class Config(object):

    # 随机种子配置
    RANDOM_SEED = 42
    # 机器树的层数
    NODE_LAYERS = 3
    # 生成package数量/个
    NUM_PACKAGES = 10
    # 包裹生成间隔
    INTERVAL_TIME = 1
    # 包裹传送带类型
    TYPE_PIP_LINE = Store
    ID_LAST_MACHINE = ['package_generator']
    # 测试机器id表
    ID_TEST_MACHINE = ['test_machine_1', 'test_machine_2', 'test_machine_3', 'test_machine_4']
    # 测试机器入口数量
    TEST_MACHINE_INPUT_PORT_NUM = ['port_1', 'port_2']
    # 测试机器资源
    TEST_MACHINE_RESOURCE = 0
    # 根据测试机器后面可能去的机器ID配置, 其实为侧机器出口数量
    ID_NEXT_MACHINE = ['next_machine_1', 'next_machine_2', 'next_machine_3', 'next_machine_4']

    def __init__(self):
        pass

    @staticmethod
    def init_app(app):
        pass
