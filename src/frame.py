# -*- coding: utf-8 -*-

from tkinter import Frame


class App(Frame):
    """"""
    def __init__(self, master=None, pack: dict=None, attr: dict=None):
        super().__init__(master=master)
        self.pack_dic = pack
        self.attr = attr
        self._init_frame()

    def _init_frame(self):
        if self.pack_dic:
            self.pack(self.pack_dic)
        else:
            self.pack()
        if self.attr:
            self.config(self.attr)
    def reset_pack(self):
        """"""
        pass
