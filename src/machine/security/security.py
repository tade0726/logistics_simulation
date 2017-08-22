# -*- coding: utf-8 -*-
"""
==================================================================================================================================================
                                                     杭州HUB仿真项目
                                    项目启动日期：2017年7月6日
                                    项目启动标识：AIRPORT OF EZHOU'S PROJECT  -- HZ
                                    ===========================================
                                    代码创建日期：2017年7月31日
                                    代码创建工程师：谈和
                                    代码版本：1.0
                                    版本更新日期：
                                    版本更新工程师：
                                    代码整体功能描述：安检模块；
==================================================================================================================================================
"""
import simpy

from src.vehicles.items import Package
from src.config import LOG
from src.utils import PackageRecordDict
from src.machine import BaseMachine

class Security(BaseMachine):
    """
     安检机的仿真
     """

    def __init__(self,
                 env,
                 machine_id,
                 pipelines_dict=None,
                 resource_dict=None,
                 equipment_resource_dict=None):
        super(Security, self).__init__(env)
        self.machine_id = machine_id
        # 队列字典
        self.pipelines_dict = pipelines_dict
        # 资源字典
        self.resource_dict = resource_dict
        # 机器资源id与机器id映射字典
        self.equipment_resource_dict = equipment_resource_dict

        # 初始化初分拣字典
        self.resource_set = self._set_machine_resource()

    def _set_machine_resource(self):
        """"""
        if self.equipment_resource_dict:
            self.equipment_id = self.machine_id[1]
            self.resource_id = self.equipment_resource_dict[self.equipment_id]
            self.resource = self.resource_dict[self.resource_id]['resource']
            self.process_time = self.resource_dict[self.resource_id]['process_time']
            self.input_pip_line = self.pipelines_dict[self.machine_id]

        else:
            raise RuntimeError('cross machine',
                               self.machine_id,
                               'not initial equipment_resource_dict!')

    def processing(self, package: Package):
        # 请求资源（工人)
        with self.resource.request() as req:
            yield req
            # 记录机器开始处理货物信息
            package.insert_data(
                PackageRecordDict(
                    equipment_id=self.equipment_id,
                    time_stamp=self.env.now,
                    action="start", ))
            # 增加处理时间
            yield self.env.timeout(self.process_time)

            # 记录机器结束处理货物信息
            package.insert_data(
                PackageRecordDict(
                    equipment_id=self.equipment_id,
                    time_stamp=self.env.now,
                    action="end", ))
            # 放入下一步的传送带
            try:
                # 重新规划安检路径
                package.set_path(package_start=self.equipment_id)
                self.pipelines_dict[package.next_pipeline].put(package)
            except Exception as exc:
                self.pipelines_dict['error'].put(package)
                msg = f"error: {exc}, package: {package}, equipment_id: {self.equipment_id}"
                LOG.logger_font.error(msg)
                LOG.logger_font.exception(exc)

    def run(self):
        while True:
            try:
                package = yield self.input_pip_line.get()
            except simpy.Interrupt:
                self.close = True
                LOG.logger_font.debug(f"sim time: {self.env.now} - equipment: {self.equipment_id} - close 1800s")
                yield self.env.timeout(1800)
                break

            # 有包裹就推送到资源模块
            self.env.process(self.processing(package))
