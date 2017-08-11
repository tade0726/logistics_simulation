# -*- coding: utf-8 -*-

from tkinter import Frame
from tkinter.ttk import Combobox
from tkinter import Checkbutton
from tkinter import Entry, IntVar, StringVar
from .frame_r_view import ConfigCheckBtn, DATABASES, BTN_ENTRY_DICT, \
    ENTRY_STATUS_DIC

from pymysql import connect


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


def init_check_btn(master, id, var, command):
    """"""
    return CheckBtnCreate(
        master=master,
        grid_dic=ConfigCheckBtn.CHECK_BTN[id]['grid'],
        attr_dic=ConfigCheckBtn.CHECK_BTN[id]['attr'],
        id=id,
        var=var,
        command=command
    )


def init_entry(master, id, text_var):
    """

    :param master:
    :param id:
    :param text_var:
    :return:
    """
    return EntryCreate(
        master=master,
        attr_dic=ConfigCheckBtn.ENTRY[id]['attr'],
        grid_dic=ConfigCheckBtn.ENTRY[id]['grid'],
        text_var=text_var
    )


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


class CheckBtnEntry(object):

    def __init__(self, w_id, master):
        self.w_id = w_id
        self.master = master
        self.var = IntVar()
        self.string = StringVar()
        self.entry = self.init_entry()
        self.check_btn = self.init_check_btn()

    def init_list(self):
        pass

    def init_entry(self):
        return init_entry(
            master=self.master,
            id=self.w_id,
            text_var=self.string
        )

    def init_check_btn(self):
        return init_check_btn(
            master=self.master,
            id=self.w_id,
            var=self.var,
            command=self.chk_button_value
        )

    def init_on_off_status(self):
        self.var.set(BTN_ENTRY_DICT[self.w_id])
        self.string.set(ENTRY_STATUS_DIC[self.var.get()])
        if self.string.get() == 'ON':
            self.entry['disabledforeground'] = 'blue'

    def chk_button_value(self):
        self.string.set(ENTRY_STATUS_DIC[self.var.get()])
        if self.string.get() == 'ON':
            self.entry['disabledforeground'] = 'blue'
        else:
            self.entry['disabledforeground'] = 'SystemDisabledText'
