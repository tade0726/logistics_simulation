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
                                    版本更新日期：2017年7月20日
                                    版本更新工程师：卢健，赵鹏

                                    代码整体功能描述：汇流点机器类模块
                                                      1、二入一出模型， 本次只需要一个入口一个出口；
                                                      2、无延时处理过程；
                                                      3、每个入口\出口无服务受限；
=====================================================================================================
"""

from sim.utils import PackageRecordDict
from sim.config import LOG


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
                 equipment_port,
                 pipelines_dict: dict,
                 resource_dict: dict,
                 equipment_resource_dict: dict,
                 share_queue_dict: dict):
        """
        init class self args:
        Args:
            env: A simpy.Environment instance.
            equipment_port: Cross machine id.
            pipelines_dict: pip line 字典
            resource_dict: 资源查询字典
            equipment_resource_dict: 机器资源id映射字典
        Raises:
            RuntimeError: An error occurred when input_dic
            not initialized before.
        """
        self.env = env
        self.equipment_port = equipment_port
        self.pipelines_dict = pipelines_dict
        self.equipment_resource_dict = equipment_resource_dict
        self.resource_dict = resource_dict
        self.share_queue_dict = share_queue_dict

        self.resource_set = self._set_machine_resource()

    def _set_machine_resource(self):
        """"""
        if self.equipment_resource_dict:
            self.input_pip_line = self.share_queue_dict[self.equipment_port]
        else:
            raise RuntimeError('cross machine',
                               self.equipment_port,
                               'not initial equipment_resource_dict!')

    def run(self):

        while True:
            # 请求货物
            package = yield self.input_pip_line.get()
            # 记录机器开始处理货物信息
            package.insert_data(
                PackageRecordDict(
                    equipment_id=self.equipment_port,
                    time_stamp=self.env.now,
                    action="start", ))
            # 记录机器结束处理货物信息
            package.insert_data(
                PackageRecordDict(
                    equipment_id=self.equipment_port,
                    time_stamp=self.env.now,
                    action="end", ))
            # 放入下一步的传送带
            try:
                self.pipelines_dict[package.next_pipeline].put(package)
            except Exception as exc:
                self.pipelines_dict['error'].put(package)
                msg = f"error: {exc}, package: {package}, equipment_id: {self.equipment_port}"
                LOG.logger_font.error(msg)
                LOG.logger_font.exception(exc)