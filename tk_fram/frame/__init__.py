# -*- coding: utf-8 -*-

from tkinter import Tk
from .frame_app import init_r_frame, init_menu
# from .frame_api import menu_file
from .frame_view import FRAME_WIDTH, FRAME_HEIGHT


def create_frame():
    """"""
    #  =======================添加主视图====================
    root = Tk()
    # ============================文件批量配置=============================
    # 标题
    menu_bar = init_menu(root)
    # =======================配置主视图尺寸=================
    root.geometry(f"{FRAME_WIDTH}x{FRAME_HEIGHT}+0+0")
    root.title('云镜·杭v1.1功能界面')
    root.rowconfigure(0, weight=1)
    root.columnconfigure((0, 1), weight=1)
    # root.minsize(FRAME_WIDTH, FRAME_HEIGHT)
    # root.maxsize(FRAME_WIDTH, FRAME_HEIGHT)
    #  =======================config主界面=================
    root.config(
        menu=menu_bar,
        background='#A2B5CD',
    )
    #  =======================初始化r路侧界面================
    init_r_frame(root=root)
    #  =======================启动主界面====================
    root.mainloop()
