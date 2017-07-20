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

                                    代码整体功能描述：汇流点机器类模块
                                                      1、二入一出模型， 本次只需要一个入口一个出口；
                                                      2、无延时处理过程；
                                                      3、每个入口\出口无服务受限；
=====================================================================================================
"""
from src.vehicles.items import Pipeline
from src.vehicles.items import Package
from src.utils import PackageRecord


class Cross(object):
    """
    Cross obj:
    sim one machine that have more than one input ports and one out put port.
    input_i wrapped in a dict: input_dic =
    {
    'x1_in1': queue, ...,
    'x1_ini': queue}.
                  _ _ _ _ _ _ _
                 |             |
     input_1 - ->|             |
         .       |    Cross    |- ->output
     input_i - ->|             |
                 |_ _ _ _ _ _ _|
    """
    def __init__(self,
                 env,
                 machine_id,
                 input_pip_line=None,
                 pipelines_dict=None,
                 resource_dict=None,
                 equipment_resource_dict=None):
        """
        init class self args:
        Args:
            env: A simpy.Environment instance.
            machine_id: Cross machine id.
            equipment_id: 预留参数
            input_pip_line: A simpy.PriorityStore which was put from
                            ahead machine.
            pipelines_dict: pip line 字典
            equipment_resource_dict: 机器资源id映射字典
            resource_dict: 资源查询字典
        Raises:
            RuntimeError: An error occurred when input_dic
            not initialized before.
        """
        self.env = env
        self.machine_id = machine_id
        self.pipelines_dict = pipelines_dict
        self.equipment_resource_dict = equipment_resource_dict
        self.resource_dict = resource_dict
        self.resource_set = self._set_machine_resource()

    def _set_machine_resource(self):
        """"""
        if self.equipment_resource_dict:
            self.equipment_id = self.machine_id[1]
            self.input_pip_line = self.pipelines_dict[self.machine_id]
        else:
            raise RuntimeError('cross machine',
                               self.machine_id,
                               'not initial equipment_resource_dict!')

    def run(self):

        while True:
            package = yield self.input_pip_line.get()
            # 获取出口队列id
            id_output_pip_line = package.next_pipeline
            # 记录机器开始处理货物信息
            package.insert_data(
                PackageRecord(
                    equipment_id=self.equipment_id,
                    package_id=package.item_id,
                    time_stamp=self.env.now,
                    action="start", ))
            # 记录机器结束处理货物信息
            package.insert_data(
                PackageRecord(
                    equipment_id=self.equipment_id,
                    package_id=package.item_id,
                    time_stamp=self.env.now,
                    action="end", ))
            # 放入下一步的传送带
            self.pipelines_dict[id_output_pip_line].put(package)