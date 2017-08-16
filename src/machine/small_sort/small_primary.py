# -*- coding: utf-8 -*-
"""
==================================================================================================================================================
                                                     杭州HUB仿真项目
                                    项目启动日期：2017年7月6日
                                    项目启动标识：AIRPORT OF EZHOU'S PROJECT  -- HZ
                                    ===========================================
                                    代码创建日期：2017年7月25日
                                    代码创建工程师：谈和
                                    代码版本：1.0
                                    版本更新日期：
                                    版本更新工程师：
                                    代码整体功能描述：小件分拣机的拆包模块；
==================================================================================================================================================
"""
from src.vehicles.items import SmallBag
from src.utils import PackageRecord
from src.config import LOG


class SmallPrimary(object):
    """
    小件拆包机的仿真
    """
    def __init__(self,
                 env,
                 machine_id,
                 pipelines_dict=None,
                 resource_dict=None,
                 equipment_resource_dict=None):
        """
        """
        self.env = env
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

    def processing(self, small_bag: SmallBag):
        assert isinstance(small_bag, SmallBag), "Wrong Type of package"
        # 请求资源（工人)，一个工人处理一个小件包
        with self.resource.request() as req:
            yield req
            # 获取小件包中的所有小件
            small_packages = small_bag.get_all_package()

            # record for small bag
            small_bag.insert_data(
                PackageRecord(
                    equipment_id=self.equipment_id,
                    package_id=small_bag.item_id,
                    time_stamp=self.env.now,
                    action="start", ), to_small=False)

            for small_package in small_packages:
                # 记录机器开始处理货物信息
                small_package.insert_data(
                    PackageRecord(
                        equipment_id=self.equipment_id,
                        package_id=small_package.item_id,
                        time_stamp=self.env.now,
                        action="start", ))
                # 增加处理时间
                yield self.env.timeout(self.process_time)
                # 记录机器结束处理货物信息
                small_package.insert_data(
                    PackageRecord(
                        equipment_id=self.equipment_id,
                        package_id=small_package.item_id,
                        time_stamp=self.env.now,
                        action="end", ))
                # 生成小件的路径
                try:
                    small_package.set_path(self.equipment_id)
                    # 放入下一步的传送带
                    self.pipelines_dict[small_package.next_pipeline].put(small_package)
                except Exception as exc:
                    self.pipelines_dict["small_primary_error"].put(small_package)
                    msg = f"error: {exc}, package: {small_package}, equipment_id: {self.equipment_id}"
                    LOG.logger_font.error(msg)
                    LOG.logger_font.exception(exc)
                    # 收集错错误的小件包裹

            # record for small bag
            small_bag.insert_data(
                PackageRecord(
                    equipment_id=self.equipment_id,
                    package_id=small_bag.item_id,
                    time_stamp=self.env.now,
                    action="end", ), to_small=False)

            # collect small bag of the first state
            self.pipelines_dict['small_bag_done'].put(small_bag)

    def run(self):
        while True:
            small_bag = yield self.input_pip_line.get()
            # 有包裹就推送到资源模块
            self.env.process(self.processing(small_bag))
