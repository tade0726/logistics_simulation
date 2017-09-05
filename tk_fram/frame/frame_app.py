# -*- coding: utf-8 -*-

from tkinter import Tk, Label, Button, Text, StringVar, Menu
from tkinter.ttk import Combobox
from .frame import App
from .frame_view import *
# import logging as lg
from .db_api import init_btn_entry_val_from_sql, init_day_time
from .frame_api import run_sim, update_data, q_exit, menu_file, \
    create_canvas, init_sheet, set_during_time, update_time_date, \
    update_to_cache, reverse


def init_app(master, wig, xlayout=(0, ), ylayout=(0, )):
    """"""
    return App(master=master,
               pack=ConfigApp.RELOAD_FRAME[wig]['grid'],
               attr=ConfigApp.RELOAD_FRAME[wig]['attr'],
               xlayout=xlayout,
               ylayout=ylayout
               )


def init_menu(root: Tk):
    base_menu = Menu(root)
    file_set_menu = Menu(master=base_menu, tearoff=0)
    file_set_menu.add_command(label='退出', command=root.quit)
    base_menu.add_cascade(label='文件', menu=file_set_menu)
    # ==========================仿真设置menu=======================
    sim_set_menu = Menu(master=base_menu, tearoff=0)
    sim_set_menu.add_command(
        label='单时段批量设置',
        command=menu_file
    )
    # sim_set_menu.add_command(
    #     label='全时段批量设置',
    #     command=lambda: menu_file(root)
    # )
    base_menu.add_cascade(label='仿真配置', menu=sim_set_menu)
    return base_menu


def init_r_frame(root: Tk):
    """"""

    config_view = CheckBtnEntryView()
    config_view.init_view()
    #  =================左侧设置基底面板===============
    left = init_app(
        master=root, wig='LEFT_FRAME', ylayout=(0, 1, 2)
    )
    #  =================右侧输出基底面板===============
    right = init_app(
        master=root,
        wig='RIGHT_FRAME',
        ylayout=(0, 1, 2)
    )
    #  ================左侧包裹数，人力资源数 ==========
    left_set_pad_package = init_app(
        master=left,
        wig='LEFT_SET_PAD_TOP_PACKAGE',
        xlayout=tuple(i for i in range(6))
    )
    #  ================左侧r 表头 ==========
    left_set_pad_sheet = init_app(
        master=left,
        wig='LEFT_SET_PAD_SHEET',
        xlayout=tuple(i for i in range(6))
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
        wig='RIGHT_BUTTON',
        xlayout=(0, 1, 2, 3)
    )
    #  ==============右侧中部输出面板样式===============
    right_output_pad_info = init_app(
        master=right,
        wig='RIGHT_OUTPUT_PAD_INFO'
    )
    # ========================= 初始化时间参数 =======================
    init_day_time()
    #  =============查询机器开关状态：from mysql 配置数据=============
    init_btn_entry_val_from_sql()
    # ============================包裹设置参数========================
    lbl_package = Label(
        master=left_set_pad_package,
        font=('Times', 10, 'bold'),
        text='仿真件量：',
        bd=8,
        # height=3,
        # width=15,
        anchor='w'
    )
    lbl_package.grid(row=0, column=0, sticky='nswe')
    package_num = Combobox(
        master=left_set_pad_package,
        # bd=8,
        # height=2,
        width=15,
        textvariable=StringVar(),
        values=PACKAGE_NUM_LIST
    )
    package_num.grid(row=0, column=1)
    # ============================班次时间配置=============================
    # -----------------------日期表标题
    lbl_date_plan = Label(
        master=left_set_pad_package,
        font=('Times', 10, 'bold'),
        text='日期：',
        bd=8,
        # height= 3,
        anchor='w'
    )
    lbl_date_plan.grid(row=0, column=2, sticky='nswe')
    date_list = list(DAY_TIME_DICT.keys())
    date_list.sort()
    date_plan = Combobox(
        master=left_set_pad_package,
        width=15,
        # bd=8,
        # height=2,
        textvariable=StringVar(),
        values=date_list,
    )
    date_plan.set(CURRENT['TIME']['date'])
    date_plan.bind("<<ComboboxSelected>>",
                   lambda x: set_during_time(date_plan, time_plan))
    date_plan.grid(row=0, column=3)
    # -----------------------时间表标题
    lbl_time = Label(
        master=left_set_pad_package,
        font=('Times', 10, 'bold'),
        text='时段：',
        bd=8,
        # height= 3,
        anchor='w'
    )
    lbl_time.grid(row=0, column=4, sticky='nswe')
    time_plan = Combobox(
        master=left_set_pad_package,
        width=15,
        # bd=8,
        # height=2,
        textvariable=StringVar(),
        values=DAY_TIME_DICT[CURRENT['TIME']['date']],
        postcommand=update_to_cache
    )
    time_plan.set(CURRENT['TIME']['time'])
    time_plan.bind("<<ComboboxSelected>>",
                   lambda x: update_time_date(date_plan, time_plan))
    time_plan.grid(row=0, column=5)
    # ===================  机器区域sheet      =====================
    for _ in init_sheet(left_set_pad_sheet, left_set_pad_center_up):
        pass

    # ===================     卸货区数据      =====================
    CURRENT['CANVAS_DICT']['canvas'], CURRENT['CANVAS_DICT']['scrollbar'] = \
        create_canvas(left_set_pad_center_up, 'R')
    # ============================仿真结果输出面板======================
    lbl_info = Label(
        master=right_output_pad_title,
        font=('arial', 12, 'bold'),
        text='输出结果统计',
        # bd=2,
        anchor='w'
    )
    lbl_info.grid(row=0, column=0, sticky='nswe')
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
    txt_receipt.grid(row=1, column=0, sticky='nswe')
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
            root, txt_receipt
        )
    ).grid(row=0, column=0, sticky='nswe')
    # 启动仿真按钮
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="启动仿真",
        command=lambda: run_sim(package_num, root, txt_receipt)
    ).grid(row=0, column=1, sticky='nswe')
    # btn-重置数据
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="恢复默认",
        command=lambda: reverse(
            root, txt_receipt
        )
    ).grid(row=0, column=2, sticky='nswe')
    # btn-退出按钮
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="退出",
        command=lambda: q_exit(root)
    ).grid(row=0, column=3, sticky='nswe')
    # ========================================================
