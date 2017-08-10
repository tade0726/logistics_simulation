# -*- coding: utf-8 -*-

from tkinter import Tk, Label, Entry, Button, Spinbox, Text, Canvas, Y, BOTH, \
    YES, Frame, Scrollbar
from .frame import App, CheckBtnEntry
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
    left_set_pad_title = init_app(
        master=left,
        wig='LEFT_SET_PAD_TITLE'
    )

    left_set_pad_left_title = init_app(
        master=left_set_pad_title,
        wig='LEFT_SET_PAD_LEFT_TITLE'
    )
    #
    left_set_pad_right_title = init_app(
        master=left_set_pad_title,
        wig='LEFT_SET_PAD_RIGHT_TITLE'
    )
    #  ==============左侧，左部L2L设置面板样式==========
    left_set_pad_center_left = init_app(
        master=left,  # left_set_pad_r,
        wig='LEFT_SET_PAD_CENTER_LEFT'
    )
    left_set_pad_center_right = init_app(
        master=left,  # left_set_pad_r,
        wig='LEFT_SET_PAD_CENTER_RIGHT'
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

    # ==================================================
    canvas_left = Canvas(left_set_pad_center_left)
    scrollbar = Scrollbar(left_set_pad_center_left)
    scrollbar.config(command=canvas_left.yview)
    canvas_left.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill=Y)
    canvas_left.config(
        width=160,
        height=480
    )
    canvas_left.pack(
        side="left",
        expand=YES,
        fill=BOTH
    )

    frame_left = Frame(canvas_left, width=50, height=100)
    frame_left.pack(side="top", fill=BOTH)
    canvas_left.create_window(0, 0, window=frame_left, anchor="nw")

    bas = [0, 0, 0 ,100]

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
        text='仿真输入件量',
        bd=8,
        # height=3,
        anchor='w'
    )
    lbl_package.grid(row=0, column=0)
    package_num = Entry(
        master=left_set_pad_package,
        bd=8,
        # height=2,
        # width=2
    )
    package_num.grid(row=0, column=1)
    # ============================资源配置=============================
    # 标题
    lbl_resource = Label(
        master=left_set_pad_package,
        font=('Times', 10, 'bold'),
        text='初分拣区卸货口人数：',
        bd=8,
        # height= 3,
        anchor='w'
    )
    lbl_resource.grid(row=0, column=2)
    # 选择人数
    person_res = Spinbox(
        master=left_set_pad_package,
        width=31,
        bd=8,
        # height=2,
        values=(1, 2))
    person_res.grid(row=0, column=3)
    # ============================机器配置==========================
    # 路侧卸货标题-L2L
    lbl_unload = Label(
        master=left_set_pad_left_title,
        font=(
            'Times',
            12,
            'bold'
        ),
        # relief='raise',
        text='\tL2L-卸货口   ',
        # bd=8,
        anchor='w'
    )
    lbl_unload.grid(row=0, column=0)
    # 路侧卸货标题-L2L,L2A,L2S2A,L2S2L
    lbl_unload = Label(
        master=left_set_pad_right_title,
        font=(
            'Times',
            12,
            'bold'
        ),
        # relief='raise',
        text='\t\tL2L,L2A,L2S-卸货口\t\t\t\t  ',
        # bd=8,
        anchor='w'
    )
    lbl_unload.grid(row=0, column=0)

    # ===================     卸货区数据      =====================
    for w_id in ConfigCheckBtn.WIG_ID_LEFT:
        CHECK_BTN_ENTRY_DIC[w_id] = CheckBtnEntry(
            w_id, frame_left
        )
        CHECK_BTN_ENTRY_DIC[w_id].init_on_off_status()
        canvas_left["scrollregion"] = "%d %d %d %d" % \
                                      (bas[0], bas[1], bas[2], bas[3])
        bas[3] += 60

    for w_id in ConfigCheckBtn.WIG_ID_RIGHT:
        CHECK_BTN_ENTRY_DIC[w_id] = CheckBtnEntry(
            w_id, left_set_pad_center_right
        )
        CHECK_BTN_ENTRY_DIC[w_id].init_on_off_status()
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
                      width=37,
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
