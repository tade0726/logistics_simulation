# -*- coding: utf-8 -*-


from src.vehicles import Package
from random import choice


class LogicTest(object):
    """"""
    def __init__(self, env, config):
        self.env = env
        self.config = config
        self.pipline = {}
        self.pipline_dic = {}
        self.path = []

    def _path_gen(self):
        """"""
        for o in self.config.ID_LAST_MACHINE:
            tmp1 = []
            for t in self.config.ID_TEST_MACHINE:
                tmp1.append((o, t))  # (''.join([o,'_', t]))
                tmp2 = []
                for d in self.config.ID_NEXT_MACHINE:
                    tmp2.append((t, d))  # (''.join([t, '_', d]))
                    self.path.append((o, t, d))
                self.pipline_dic[t] = tmp2
            self.pipline_dic[o] = tmp1

    def _pipline_generator(self):
        for pid in self.pipline_dic.values():
            for v in pid:
                pip_line = self.config.TYPE_PIP_LINE
                self.pipline.update({v: pip_line(self.env, 10, v)})

    def generator(self):
        """"""
        self._path_gen()
        self._pipline_generator()

    def packages_generator(self):
        """"""
        for num in range(self.config.NUM_PACKAGES):
            yield self.env.timeout(self.config.INTERVAL_TIME)
            package = Package(self.env, {'id': num}, num, choice(self.path))
            # 更新货物路由
            package.pop_mark()
            # 获取package对应队列
            pip_line = self.pipline[package.next_pipeline]
            # 将货物推送到货物归属队列
            pip_line.put(package)
            print(f'<---- package {num} was pushed into '
                  f'{package.next_pipeline} at {self.env.now}')

    def get_input_pip_line(self, id_test_machine):
        """"""

        if_find = False
        for gi in self.config.ID_LAST_MACHINE:
            for pip in self.pipline_dic[gi]:
                if pip[1] == id_test_machine:
                    return self.pipline[pip]
                else:
                    continue
        if not if_find:
            raise ValueError('test machine id error!')

    def get_reusource_dic(self):
        """"""
        return {tr: self.config.TEST_MACHINE_RESOURCE for tr in
                self.config.ID_TEST_MACHINE}
