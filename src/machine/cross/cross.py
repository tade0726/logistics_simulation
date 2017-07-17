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
                 equipment_id,
                 input_pip_line=None,
                 pipelines_dict=None,
                 resource_dict=None):
        """
        init class self args:
        Args:
            env: A simpy.Environment instance.
            machine_id: Cross machine id.
            equipment_id: 预留参数
            input_pip_line: A simpy.PriorityStore which was put from
                            ahead machine.
            pipelines_dict: pip line 字典
            resource_dict: 资源查询字典
        Raises:
            RuntimeError: An error occurred when input_dic
            not initialized before.
        """
        self.env = env
        self.machine_id = machine_id
        self.equipment_id = equipment_id
        self.input_pip_line = input_pip_line
        self.pipelines_dict = pipelines_dict
        self.resource_dict = resource_dict
        self.process = self._get_package_queue()

    def _get_package_queue(self):
        """
        获取输入队列功能单元
        """
        if self.input_pip_line:
            if isinstance(self.input_pip_line, Pipeline):
                self.env.process(self._get_packages(self.input_pip_line))
        else:
            raise RuntimeError('Please Initial input pip line '
                               'Queue for Cross instance First!')

    def _get_packages(self, get_package_queue):
        """
        """
        while True:
            packages = yield get_package_queue.get()
            # 判断取没取到货物
            if packages:
                print(f"------->package {packages.item['package_id']}",
                      'was push to next queue at', self.env.now)
                self.env.process(self._put_packages_into_out_queue(packages))

    def _put_packages_into_out_queue(self, package):
        """
        """
        if isinstance(package, Package):
            id_output_pip_line = package.next_pipeline
            yield self.pipelines_dict[id_output_pip_line].put(package)
