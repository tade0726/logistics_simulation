# -*- coding: utf-8 -*-

from tkinter import Frame
from tkinter.ttk import Combobox
from tkinter import Checkbutton, Entry, Menu
from tkinter import IntVar, StringVar, DISABLED, NORMAL
from .frame_r_view import ConfigFrame, \
    ENTRY_STATUS_DIC, M_R_DICT, CACHE_INSTANCE_DICT, M_J_DICT, CACHE_J_STATUS


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

    @property
    def _list_value(self):
        if self.w_id == 'j41_1' or self.w_id == 'h3_1':
            return self.list_value[1]
        if 'j' in self.w_id or 'h' in self.w_id:
            return self.list_value[0]
        return self.list_value

    def init_list(self):
        return init_combobox_list(
            master=self.master,
            id=self.w_id,
            string_combobox=self.string_combobox,
            list_var=self._list_value
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
        self.set_status(CACHE_INSTANCE_DICT)

    def set_status(self, status_dict):
        if self.w_id == 'j41_1' or 'h' in self.w_id:
            self.var.set(1)
            self.string.set(ENTRY_STATUS_DIC[1])
            self.string_combobox.set(CACHE_INSTANCE_DICT[self.w_id]['num'])
            self.check_btn['state'] = DISABLED
            self.change_color(self.entry)
        elif 'm' in self.w_id or 'j' in self.w_id:
            # 判定 J 是否有缓存值且缓存值是否有效，否则取初始值(M 默认不匹配)
            if self.w_id in CACHE_J_STATUS and \
                            CACHE_J_STATUS[self.w_id] != self.check_var:
                self.var.set(CACHE_J_STATUS[self.w_id])
            else:
                self.var.set(self.check_var)
            self.string.set(ENTRY_STATUS_DIC[self.var.get()])
            self.change_combobox_status(self)
            self.change_color(self.entry)
            if 'm' in self.w_id:
                self.check_btn['state'] = DISABLED
            if 'j' in self.w_id:
                # 根据初始化的值判断是否为 DISABLED
                if self.check_var == 0 :
                    self.check_btn['state'] = DISABLED
                else:
                    self.check_btn['state'] = NORMAL
        else:
            self.var.set(status_dict[self.w_id]['status'])
            self.string.set(ENTRY_STATUS_DIC[self.var.get()])
            self.change_combobox_status(self)
            self.change_color(self.entry)

    def chk_button_value(self):
        # j 由 ON 改为 OFF 时将会添加到 J的缓存字典里
        if 'j' in self.w_id:
            if self.var.get() == 0:
                CACHE_J_STATUS[self.w_id] = self.var.get()
            else:
                CACHE_J_STATUS.pop(self.w_id)

        self.string.set(ENTRY_STATUS_DIC[self.var.get()])
        self.change_color(self.entry)
        self.change_combobox_status(self)

    # 返回勾选框的状态值 0 或 1
    @property
    def check_var(self):
        return _init_m_J(self.w_id)

    @staticmethod
    def change_color(entry):
        if entry.text_var.get() == 'ON':
            entry['disabledforeground'] = 'blue'
        else:
            entry['disabledforeground'] = 'SystemDisabledText'

    @staticmethod
    def change_combobox_status(instance):
        instance.string_combobox.set(CACHE_INSTANCE_DICT[instance.w_id]['num'])
        if instance.var.get() == 0:
            instance.init_list['state'] = DISABLED
        else:
            instance.init_list['state'] = NORMAL

def _init_m_J(w_id):
    if 'm' in w_id:
        status = 0
        for i in M_R_DICT[w_id]:
            status = CACHE_INSTANCE_DICT[i]['status'] or status
        return status
    if 'j' in w_id and w_id != 'j41_1':
        j_status = 0
        for key, j_list in M_J_DICT.items():
            if w_id in j_list:
                for r_id in M_R_DICT[key]:
                    j_status = CACHE_INSTANCE_DICT[r_id]['status'] or j_status
        return j_status

def update_m_j():
    # 根据 R 的状态值，初始化 J 跟 M 的状态值，如果 J 有缓存，则取缓存值
    for j in ConfigFrame.WIG_BTN_DICT['J'][:-1]:
        if j in CACHE_J_STATUS:
            CACHE_INSTANCE_DICT[j]['status'] = CACHE_J_STATUS[j]
        else:
            CACHE_INSTANCE_DICT[j]['status'] = _init_m_J(j)
    for m in ConfigFrame.WIG_BTN_DICT['M']:
        CACHE_INSTANCE_DICT[m]['status'] = _init_m_J(m)