# -*- coding: utf-8 -*-

from tkinter import Frame
from tkinter import Checkbutton
from tkinter import Entry


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


class CheckBtnCreate(Checkbutton):
    """"""
    def __init__(
            self,
            master=None,
            grid_dic: dict=None,
            attr_dic: dict=None,
            id: str='',
            var=None,
            command=None
    ):
        """"""
        super().__init__(master=master)
        self.grid_dic = grid_dic
        self.attr_dic = attr_dic
        self.text = id
        self.var = var
        self.command = command
        self._update_config()
        self._init_check_btn()

    def _update_config(self):
        self.attr_dic.update({
            'text': self.text,
            'variable': self.var,
            'command': self.command})


    def _init_check_btn(self):
        """"""
        if self.attr_dic:
            self.config(self.attr_dic)
        if self.grid_dic:
            self.grid(self.grid_dic)
        else:
            self.grid()

    def append_cls(
            self,
            cls=Entry,
            var=None,
            attr: dict=None,
            grid: dict=None
    ):
        """附加"""
        return_cls = cls(master=self.master)
        attr_config = attr.update({
            'textvariable': var})
        return_cls.config(attr_config)
        return_cls.grid(grid)

        return return_cls


class EntryCreate(Entry):
    """"""
    def __init__(
            self,
            master=None,
            grid_dic: dict=None,
            attr_dic: dict=None,
            text_var=None,
    ):
        super().__init__(master=master)
        self.attr_dic = attr_dic
        self.grid_dic = grid_dic
        self.text_var = text_var
        self._update_config()
        self._init_entry()

    def _update_config(self):
        self.attr_dic.update(
            {
                'textvariable': self.text_var
            }
        )

    def _init_entry(self):
        """"""
        if self.attr_dic:
            self.config(self.attr_dic)
        #
        if self.grid_dic:
            self.grid(self.grid_dic)
        else:
            self.grid()
