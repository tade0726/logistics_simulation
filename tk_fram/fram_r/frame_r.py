# -*- coding: utf-8 -*-

from tkinter import Tk, Label, Entry, Button, Text, Canvas, Y, BOTH, \
    YES, Frame, Scrollbar, StringVar, Menu, Checkbutton
from tkinter.ttk import Combobox
from .frame import App, CheckBtnEntryList
from .frame_r_view import *
# import logging as lg
from .db_api import init_btn_entry_val_from_sql
from .frame_api import run_sim, save_data, update_data, q_exit, menu_file


def init_app(master, wig):
    """"""
    return App(master=master,
               pack=ConfigApp.RELOAD_FRAME[wig]['pack'],
               attr=ConfigApp.RELOAD_FRAME[wig]['attr'])


def init_menu(root: Tk):
    base_menu = Menu(root)
    file_set_menu = Menu(master=base_menu, tearoff=0)
    file_set_menu.add_command(label='退出', command=root.quit)
    base_menu.add_cascade(label='文件', menu=file_set_menu)
    # ==========================仿真设置menu=======================
    sim_set_menu = Menu(master=base_menu, tearoff=0)
    sim_set_menu.add_command(
        label='单时段批量设置',
        command=lambda: menu_file(root)
    )
    sim_set_menu.add_command(
        label='全时段批量设置',
        command=lambda: menu_file(root)
    )
    base_menu.add_cascade(label='仿真配置', menu=sim_set_menu)
    return base_menu


def init_r_frame(root: Tk):
    """"""

    config_view = CheckBtnEntryView()
    config_view.init_view()
    #  =================左侧设置基底面板===============
    left = init_app(
        master=root, wig='LEFT_FRAME'
    )
    #  =================右侧输出基底面板===============
    right = init_app(
        master=root,
        wig='RIGHT_FRAME'
    )
    #  ================左侧包裹数，人力资源数 ==========
    left_set_pad_package = init_app(
        master=left,
        wig='LEFT_SET_PAD_TOP_PACKAGE'
    )
    #  ================左侧r 表头 ==========
    left_set_pad_sheet = init_app(
        master=left,
        wig='LEFT_SET_PAD_SHEET'
    )
    #  ==============左侧，设置面板==========
    left_set_pad_center_up = init_app(
        master=left,  # left_set_pad_r,
        wig='LEFT_SET_PAD_CENTER_UP'
    )
    #  ===============右侧输出标题样式=================
    right_output_pad_title = init_app(
        master=right,
        wig='RIGHT_TITLE'
    )
    # =============右侧下部按钮控件样式===============
    right_output_pad_button = init_app(
        master=right,
        wig='RIGHT_BUTTON'
    )
    #  ==============右侧中部输出面板样式===============
    right_output_pad_info = init_app(
        master=right,
        wig='RIGHT_OUTPUT_PAD_INFO'
    )
    #  =============查询机器开关状态：from mysql 配置数据=============
    init_btn_entry_val_from_sql()

    # ======================left- top1============================
    #
    canvas_up = Canvas(left_set_pad_center_up)
    scrollbar_up = Scrollbar(left_set_pad_center_up)
    scrollbar_up.config(command=canvas_up.yview)
    canvas_up.config(yscrollcommand=scrollbar_up.set)
    scrollbar_up.pack(side="right", fill=Y)
    canvas_up.config(
        width=660,
        height=500
    )
    canvas_up.pack(
        side="left",
        expand=YES,
        fill=BOTH
    )

    frame_up = Frame(canvas_up, width=50, height=100)
    frame_up.pack(side="top", fill=BOTH)
    canvas_up.create_window(0, 0, window=frame_up, anchor="nw")

    bas_up = [0, 0, 0, 50]
    # ============================包裹设置参数========================
    lbl_package = Label(
        master=left_set_pad_package,
        font=('Times', 10, 'bold'),
        text='仿真输入件量：',
        bd=8,
        # height=3,
        width=15,
        anchor='w'
    )
    lbl_package.grid(row=0, column=0)
    package_num = Entry(
        master=left_set_pad_package,
        bd=8,
        # height=2,
        width=30
    )
    package_num.grid(row=0, column=1)
    # ============================班次时间配置=============================
    # 班次标题
    lbl_schedul = Label(
        master=left_set_pad_package,
        font=('Times', 10, 'bold'),
        text='班次时间表：',
        bd=8,
        # height= 3,
        anchor='w'
    )
    lbl_schedul.grid(row=0, column=2)
    #
    date = StringVar()
    schedul_plan = Combobox(
        master=left_set_pad_package,
        width=25,
        # bd=8,
        # height=2,
        textvariable=date,
        values=TIME_LIST
    )
    schedul_plan.grid(row=0, column=3)
    # ===================  机器区域sheet      =====================
    r_btn = Checkbutton(
        master=left_set_pad_sheet,
        text="R_路侧卸货区",
        variable=StringVar(),
        onvalue=1,
        offvalue=0,
        relief='raise',
        bd=5
        )
    r_btn.grid({'row':0, 'column':0})
    a_btn = Checkbutton(
        master=left_set_pad_sheet,
        text="A_空侧卸货区",
        variable=StringVar(),
        onvalue=1,
        offvalue=0,
        relief='raise',
        bd=5
    )
    a_btn.grid({'row': 0, 'column': 1})
    m_btn = Checkbutton(
        master=left_set_pad_sheet,
        text="M_初分拣矩阵",
        variable=StringVar(),
        onvalue=1,
        offvalue=0,
        relief='raise',
        bd=5
    )
    m_btn.grid({'row': 0, 'column': 2})
    j_btn = Checkbutton(
        master=left_set_pad_sheet,
        text="J_安检机",
        variable=StringVar(),
        onvalue=1,
        offvalue=0,
        relief='raise',
        bd=5
    )
    j_btn.grid({'row': 0, 'column': 3})
    u_btn = Checkbutton(
        master=left_set_pad_sheet,
        text="U_小件拆包台",
        variable=StringVar(),
        onvalue=1,
        offvalue=0,
        relief='raise',
        bd=5
    )
    u_btn.grid({'row': 0, 'column': 4})
    h_btn = Checkbutton(
        master=left_set_pad_sheet,
        text="H_医院区",
        variable=StringVar(),
        onvalue=1,
        offvalue=0,
        relief='raise',
        bd=5
    )
    h_btn.grid({'row': 0, 'column': 5})
    # ===================     卸货区数据      =====================
    for w_id in ConfigFrame.WIG_ID_R:
        CHECK_BTN_ENTRY_DIC[w_id] = CheckBtnEntryList(
            w_id,
            frame_up,
            LIST_VALUE_COMBOBOX['R']
        )
        CHECK_BTN_ENTRY_DIC[w_id].init_on_off_status()
        canvas_up["scrollregion"] = "%d %d %d %d" % (
            bas_up[0],
            bas_up[1],
            bas_up[2],
            bas_up[3]
        )
        bas_up[3] += 50/3
    # ============================仿真结果输出面板======================
    lbl_info = Label(
        master=right_output_pad_title,
        font=('arial', 12, 'bold'),
        text='输出结果统计',
        # bd=2,
        anchor='w'
    )
    lbl_info.grid(row=0, column=0)
    # ============================输出信息面板=========================
    txt_receipt = Text(
        right_output_pad_info,
        font=('Time', 13),
        height=28,
        width=37,
        bd=7,
        bg="white",
        state=DISABLED
    )
    txt_receipt.grid(row=1, column=0)
    # ===========================Button===============================
    font_btn = 10
    width_btn = 5
    btn_pady = 5
    btn_padx = 23
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="数据更新",
        command=lambda: update_data(
            package_num, schedul_plan, root, txt_receipt
        )
    ).grid(row=0, column=0)
    # 启动仿真按钮
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="启动仿真",
        command=lambda: run_sim(package_num, schedul_plan, root, txt_receipt)
    ).grid(row=0, column=1)
    # btn-存储数据按钮
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="存储数据",
        command=lambda: save_data(package_num, schedul_plan, root, txt_receipt)
    ).grid(row=0, column=2)
    # btn-退出按钮
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="退出",
        command=lambda: q_exit(root)
    ).grid(row=0, column=3)
    # ========================================================
