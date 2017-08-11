# -*- coding: utf-8 -*-

from tkinter import Tk, Label, Entry, Button, Spinbox, Text, Canvas, Y, BOTH, \
    YES, Frame, Scrollbar, StringVar
from tkinter.ttk import Combobox
from .frame import App, CheckBtnEntryList
from .frame_r_view import *
# import logging as lg
from .db_api import init_btn_entry_val_from_sql
from .frame_api import run_sim, save_data, update_data, q_exit


def init_app(master, wig):
    """"""
    return App(master=master,
               pack=ConfigApp.RELOAD_FRAME[wig]['pack'],
               attr=ConfigApp.RELOAD_FRAME[wig]['attr'])


def init_r_frame(root: Tk):
    """"""
    config_view = CheckBtnEntryView()
    config_view.init_view()
    #  ===================顶部标题面板================
    top = init_app(
        master=root, wig='TOP_FRAME'
    )
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
    #  ================左侧左标题 ==========
    # left_set_pad_title = init_app(
    #     master=left,
    #     wig='LEFT_SET_PAD_TITLE'
    # )
    #
    # left_set_pad_left_title = init_app(
    #     master=left_set_pad_title,
    #     wig='LEFT_SET_PAD_LEFT_TITLE'
    # )
    # #
    # left_set_pad_right_title = init_app(
    #     master=left_set_pad_title,
    #     wig='LEFT_SET_PAD_RIGHT_TITLE'
    # )
    #  ==============左侧，左部L2L设置面板样式==========
    left_set_pad_center_up = init_app(
        master=left,  # left_set_pad_r,
        wig='LEFT_SET_PAD_CENTER_UP'
    )
    left_set_pad_center_down = init_app(
        master=left,  # left_set_pad_r,
        wig='LEFT_SET_PAD_CENTER_DOWN'
    )
    #  ===============右侧输出标题样式=================
    right_output_pad_title = init_app(
        master=right,
        wig='RIGHT_TITLE'
    )
    #   =============右侧下部按钮控件样式===============
    right_output_pad_button = init_app(
        master=right,
        wig='RIGHT_BUTTON'
    )
    #  ==============右侧中部输出面板样式===============
    right_output_pad_info = init_app(
        master=right,
        wig='RIGHT_OUTPUT_PAD_INFO'
    )

    init_btn_entry_val_from_sql()

    # ======================left- top1============================
    canvas_up = Canvas(left_set_pad_center_up)
    scrollbar_up = Scrollbar(left_set_pad_center_up)
    scrollbar_up.config(command=canvas_up.yview)
    canvas_up.config(yscrollcommand=scrollbar_up.set)
    scrollbar_up.pack(side="right", fill=Y)
    canvas_up.config(
        width=645,
        height=250
    )
    canvas_up.pack(
        side="left",
        expand=YES,
        fill=BOTH
    )

    frame_up = Frame(canvas_up, width=50, height=100)
    frame_up.pack(side="top", fill=BOTH)
    canvas_up.create_window(0, 0, window=frame_up, anchor="nw")

    bas_up = [0, 0, 0 ,50]
    # ======================left- top2============================
    canvas_down = Canvas(left_set_pad_center_down)
    scrollbar_down = Scrollbar(left_set_pad_center_down)
    scrollbar_down.config(command=canvas_down.yview)
    canvas_down.config(yscrollcommand=scrollbar_down.set)
    scrollbar_down.pack(side="right", fill=Y)
    canvas_down.config(
        width=645,
        height=250
    )
    canvas_down.pack(
        side="left",
        expand=YES,
        fill=BOTH
    )

    frame_down = Frame(canvas_down, width=50, height=100)
    frame_down.pack(side="top", fill=BOTH)
    canvas_down.create_window(0, 0, window=frame_down, anchor="nw")

    bas_down = [0, 0, 0, 50]
    # ==================================================


    # ==============================Heading===========================
    lbl_info = Label(
        top,
        font=('Times', 12, 'bold'),
        text='\t\t\t\t\t\t\t杭州分拣中心仿真系统',
        bd=6,
        width=119,
        anchor='w'
    )
    lbl_info.grid(row=0, column=0)
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
        width=25
    )
    package_num.grid(row=0, column=1)
    # ============================资源配置=============================
    # 标题
    lbl_resource = Label(
        master=left_set_pad_package,
        font=('Times', 10, 'bold'),
        text='班次时间表：',
        bd=8,
        # height= 3,
        anchor='w'
    )
    lbl_resource.grid(row=0, column=2)
    # 选择人数
    date = StringVar()
    person_res = Combobox(
        master=left_set_pad_package,
        width=31,
        #bd=8,
        # height=2,
        textvariable=date,
        values=TIME_LIST
    )
    person_res.grid(row=0, column=3)
    # ============================机器配置==========================
    # 路侧卸货标题-L2L
    # lbl_unload = Label(
    #     master=left_set_pad_left_title,
    #     font=(
    #         'Times',
    #         12,
    #         'bold'
    #     ),
    #     # relief='raise',
    #     text='\tL2L-卸货口   ',
    #     # bd=8,
    #     anchor='w'
    # )
    # lbl_unload.grid(row=0, column=0)
    # # 路侧卸货标题-L2L,L2A,L2S2A,L2S2L
    # lbl_unload = Label(
    #     master=left_set_pad_right_title,
    #     font=(
    #         'Times',
    #         12,
    #         'bold'
    #     ),
    #     # relief='raise',
    #     text='\t\tL2L,L2A,L2S-卸货口\t\t\t\t  ',
    #     # bd=8,
    #     anchor='w'
    # )
    # lbl_unload.grid(row=0, column=0)

    # ===================     卸货区数据      =====================
    for w_id in ConfigFrame.WIG_ID_R:
        CHECK_BTN_ENTRY_DIC[w_id] = CheckBtnEntryList(
            w_id,
            frame_up,
            LIST_VALUE_COMBOBOX['R']
        )
        CHECK_BTN_ENTRY_DIC[w_id].init_on_off_status()
        canvas_up["scrollregion"] = "%d %d %d %d" % \
                                      (bas_up[0], bas_up[1], bas_up[2],
                                       bas_up[3])
        bas_up[3] += 50/3
    #
    for w_id in ConfigFrame.WIG_ID_M:
        CHECK_BTN_ENTRY_DIC[w_id] = CheckBtnEntryList(
            w_id,
            frame_down,
            LIST_VALUE_COMBOBOX['M']
        )
        CHECK_BTN_ENTRY_DIC[w_id].init_on_off_status()
        canvas_down["scrollregion"] = "%d %d %d %d" % \
                                      (bas_down[0], bas_down[1], bas_down[2],
                                       bas_down[3])
        bas_down[3] += 50/3
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
    txtReceipt = Text(right_output_pad_info,
                      font=('Time', 13),
                      height=28,
                      width=39,
                      bd=7,
                      bg="white",
                      state=DISABLED)
    txtReceipt.grid(row=1, column=0)
    # ===========================Button==============================
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
        command=lambda: update_data(package_num, person_res, root, txtReceipt)
    ).grid(row=0, column=0)
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="启动仿真",
        command=lambda: run_sim(package_num, person_res, root, txtReceipt)
    ).grid(row=0, column=1)
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="存储数据",
        command=lambda: save_data(package_num, person_res, root, txtReceipt)
    ).grid(row=0, column=2)
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="退出",
        command=lambda: q_exit(root)
    ).grid(row=0, column=3)
    # ========================================================
