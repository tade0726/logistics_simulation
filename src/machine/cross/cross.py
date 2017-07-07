# -*- coding: utf-8 -*-

"""
作者：kissf lu
日期：2017/7/7
说明：杭州项目，汇流点类模块

"""


from simpy import PriorityItem


class Cross(object):
    """
    Cross obj:
    sim one machine that have more than one input ports and one out put port.
    input_i wrapped in a dict: input_dic = {'x1_in1': queue, ..., 'x1_ini': queue}.
                  _ _ _ _ _ _ _
                 |             |
     input_1 - ->|             |
         .       |    Cross    |- ->output
     input_i - ->|             |
                 |_ _ _ _ _ _ _|

    """
    def __init__(self, env, id_x, input_dic: dict=None, out_put=None):
        """
        init class self args:
        Args:
            env: A simpy.Environment instance.
            id_x: Cross machine id.
            input_dic: A simpy.PriorityStore which was put from ahead machine.
            out_put: out .

        """
        self.env = env
        self.id_x = id_x
        self.input_dic = input_dic
        self.out_put = out_put
        self.process = self._get_package_queue()

    def _get_package_queue(self):
        """
        """
        if self.input_dic:
            print('in get package queue')
            for get_package_queue in self.input_dic.values():
                self.env.process(self._get_packages(get_package_queue))
        else:
            raise RuntimeError('Please Initial input port Queue for Cross instance First!')

    def _get_packages(self, get_package_queue):
        """
        """
        while True:
            packages = yield get_package_queue.get()
            self.env.process(self._put_packages_into_out_queue(packages))

    def _put_packages_into_out_queue(self, package):
        """
        """
        while True:
            yield self.out_put.put(PriorityItem(priority=self.env.now, item=package))

