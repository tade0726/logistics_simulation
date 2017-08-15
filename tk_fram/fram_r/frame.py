# -*- coding: utf-8 -*-

from tkinter import Frame
from tkinter.ttk import Combobox
from tkinter import Checkbutton, Entry, Menu
from tkinter import IntVar, StringVar, DISABLED, NORMAL
from .frame_r_view import ConfigFrame, BTN_ENTRY_DICT, \
    ENTRY_STATUS_DIC, CHECK_BTN_ENTRY_DIC, M_R_DICT, CACHE_BTN_ENTRY_DICT


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


class ComboboxCreate(Combobox):

    def __init__(
            self,
            master=None,
            string_combobox=None,
            list_var: list=None,
            attr_dic: dict=None,
            grid_dic: dict=None
    ):
        super().__init__(master=master)
        self.string = string_combobox
        self.list_var = list_var
        self.attr_dic = attr_dic
        self.grid_dic = grid_dic
        self._update_config()
        self._init_combobox_list()

    def _update_config(self):
        self.attr_dic.update(
            {
                'textvariable': self.string,
                'values': self.list_var
            }
        )

    def _init_combobox_list(self):
        """"""
        if self.attr_dic:
            self.config(self.attr_dic)
        #
        if self.grid_dic:
            self.grid(self.grid_dic)
        else:
            self.grid()


class EntryCreate(Entry):
    """"""

    def __init__(
            self,
            master=None,
            grid_dic: dict = None,
            attr_dic: dict = None,
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
        grid_dic=ConfigFrame.CHECK_BTN[id]['grid'],
        attr_dic=ConfigFrame.CHECK_BTN[id]['attr'],
        id=id,
        var=var,
        command=command
    )


def init_combobox_list(master, id, string_combobox, list_var):
    """

    :param master:
    :param id:
    :param string_combobox:
    :param list_var:
    :return:
    """
    return ComboboxCreate(
        master=master,
        string_combobox=string_combobox,
        list_var=list_var,
        attr_dic=ConfigFrame.COMBOBOX_LIST[id]['attr'],
        grid_dic=ConfigFrame.COMBOBOX_LIST[id]['grid']
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
        attr_dic=ConfigFrame.ENTRY[id]['attr'],
        grid_dic=ConfigFrame.ENTRY[id]['grid'],
        text_var=text_var
    )


class CheckBtnEntryList(object):

    def __init__(self, w_id, master, list_value):
        self.w_id = w_id
        self.master = master
        self.list_value = list_value
        self.var = IntVar()
        self.string = StringVar()
        self.string_combobox = StringVar()
        self.init_list = self.init_list()
        self.entry = self.init_entry()
        self.check_btn = self.init_check_btn()

    def init_list(self):
        return init_combobox_list(
            master=self.master,
            id=self.w_id,
            string_combobox=self.string_combobox,
            list_var=self.list_value
        )

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
        if self.w_id in CACHE_BTN_ENTRY_DICT:
            self.set_status(CACHE_BTN_ENTRY_DICT)
        else:
            self.set_status(BTN_ENTRY_DICT)

    def set_status(self, status_dict):
        if 'm' in self.w_id:
            self.var.set(self.check_var)
            self.string.set(ENTRY_STATUS_DIC[self.var.get()])
            self.change_combobox_status(self)
            self.check_btn['state'] = DISABLED
        else:
            self.var.set(status_dict[self.w_id])
            self.string.set(ENTRY_STATUS_DIC[self.var.get()])
            self.change_combobox_status(self)
        if self.string.get() == 'ON':
            self.entry['disabledforeground'] = 'blue'

    def chk_button_value(self):
        self.string.set(ENTRY_STATUS_DIC[self.check_var])
        self.change_color(self.entry)
        self.change_combobox_status(self)

    # 返回勾选框的状态值 0 或 1
    @property
    def check_var(self):
        if 'm' in self.w_id:
            status = 0
            for i in M_R_DICT[self.w_id]:
                status = CACHE_BTN_ENTRY_DICT[i] or status
            return status
        else:
            return self.var.get()

    @staticmethod
    def change_color(entry):
        if entry.text_var.get() == 'ON':
            entry['disabledforeground'] = 'blue'
        else:
            entry['disabledforeground'] = 'SystemDisabledText'

    @staticmethod
    def change_combobox_status(instance):
        if instance.var.get() == 0:
            instance.string_combobox.set(0)
            instance.init_list['state'] = DISABLED
        else:
            instance.init_list['state'] = NORMAL
            instance.string_combobox.set(1)