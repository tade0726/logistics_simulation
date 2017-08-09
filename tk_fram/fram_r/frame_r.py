# -*- coding: utf-8 -*-

from tkinter import messagebox, Tk, Label, Entry, Button, Spinbox, Text
from tkinter import NORMAL, END
from .frame import App, CheckBtnEntry
from simpy_lib import main
from .frame_r_view import *
# import logging as lg
from .db_api import *


import pymysql
import time
from datetime import datetime


def init_app(master, wig):
    """"""
    return App(master=master,
               pack=ConfigApp.RELOAD_FRAME[wig]['pack'],
               attr=ConfigApp.RELOAD_FRAME[wig]['attr'])


def init_r_frame(root: Tk):
    """"""
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
    #
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


    def save_data():
        if not package_num.get():
            messagebox.askyesno("Tkinter-数据更新错误", "运行错误，请输入仿真件量！")
            return
        if not person_res.get():
            messagebox.askyesno("Tkinter-数据更新错误",
                                "运行错误，请输入初分拣区卸货口人数！")
            return
        if Flag['save_data'] > 0:
            messagebox.askyesno("Tkinter-数据保存错误",
                                "数据已经保存，请勿重复操作！")
            return
        if Flag['cost_of_item'] == 0:
            messagebox.askyesno("Tkinter-数据保存错误",
                                "运行错误，请先执行仿真！")
            return
        txtReceipt['state'] = NORMAL
        txtReceipt.insert(END, '*******************************\n')
        txtReceipt.insert(END, '开始储存数据......\n')
        root.update_idletasks()
        conn = pymysql.connect(host=DATABASES['HOST'],
                               user=DATABASES['USER'],
                               passwd=DATABASES['PASSWORD'],
                               db=DATABASES['NAME'])
        cur = conn.cursor()
        save_to_past_run(cur)
        conn.commit()
        cur.close()
        conn.close()
        txtReceipt.insert(END, '数据存储完毕！\n'
                               '*******************************\n')
        txtReceipt['state'] = DISABLED
        Flag['save_data'] += 1

    def run_sim():
        """"""
        if not package_num.get():
            messagebox.askyesno("Tkinter-数据更新错误","运行错误， 请输入仿真件量！")
            return
        if not person_res.get():
            messagebox.askyesno("Tkinter-数据更新错误",
                                "运行错误，请输入初分拣区卸货口人数！")
            return
        if Flag['update_data'] == 0:
            messagebox.askyesno("Tkinter-仿真启动错误",
                                "运行错误，请先执行数据更新！")
            return
        if Flag['cost_of_item'] > 0:
            messagebox.askyesno("Tkinter-仿真启动错误",
                                "仿真已经运行完成，请勿重复操作！")
            return
        run_arg = Flag['run_time']
        conn = pymysql.connect(host=DATABASES['HOST'],
                               user=DATABASES['USER'],
                               passwd=DATABASES['PASSWORD'],
                               db=DATABASES['NAME'])
        cur = conn.cursor()
        cur.execute("truncate o_machine_table")
        cur.execute("truncate o_pipeline_table")
        cur.execute("truncate o_truck_table")
        conn.commit()

        txtReceipt['state'] = NORMAL
        txtReceipt.insert(END, '*******************************\n')
        txtReceipt.insert(END, '开始调用仿真函数......\n')
        root.update_idletasks()
        start_time = time.time()
        main(run_arg)
        run_time = '%.2f' % (time.time() - start_time)
        txtReceipt.insert(END, '仿真执行完毕\n')
        root.update_idletasks()
        time.sleep(0.5)
        txtReceipt.insert(END, '开始读取仿真结果......\n')
        root.update_idletasks()
        time.sleep(0.5)
        root.update_idletasks()
        result = read_result(cur)
        cur.close()
        conn.close()
        txtReceipt.insert(END, '*******************************\n')
        txtReceipt.insert(END, '最早到达时间:\t' +
                          check_time(result['fast_time']) + '\n')
        txtReceipt.insert(END, '最晚到达时间:\t' +
                          check_time(result['later_time']) + '\n')
        txtReceipt.insert(END, '最后一票处理时间:\t' +
                          check_time(result['last_solve_time'])
                          + '\n')
        txtReceipt.insert(END, '总处理时间(小时):\t' + '%.2f' %
                          result['total_solve_time'] + '\n')
        txtReceipt.insert(END, '仿真运行时间(秒):\t' + check_time(run_time) + '\n')
        txtReceipt['state'] = DISABLED
        root.update_idletasks()
        Flag['cost_of_item'] += 1
        Flag['save_data'] = 0


    def update_data():
        """"""
        Flag['run_time'] = datetime.now()
        run_arg = Flag['run_time']
        if not package_num.get():
            messagebox.askyesno("Tkinter-数据更新错误", "运行错误，请输入仿真件量！")
            return
        if not person_res.get():
            messagebox.askyesno("Tkinter-数据更新错误",
                                "运行错误，请输入初分拣区卸货口人数！")
            return

        conn = pymysql.connect(host=DATABASES['HOST'],
                               user=DATABASES['USER'],
                               passwd=DATABASES['PASSWORD'],
                               db=DATABASES['NAME'])
        cur = conn.cursor()

        # # #  显示结果
        txtReceipt['state'] = NORMAL
        txtReceipt.delete('1.0', END)
        root.update_idletasks()
        # ========================更改开关状态==============
        txtReceipt.insert(END, '机器开关状态更新......\n')
        update_on_off(cur, run_arg)
        conn.commit()
        txtReceipt.insert(END, '机器开关状态更新成功！\n')
        root.update_idletasks()
        time.sleep(0.5)
        # ======================== 插入测试数据=============
        txtReceipt.insert(END, '插入%s件包裹仿真数据......\n' % package_num.get())
        insert_package(cur, package_num.get(), run_arg)
        conn.commit()
        txtReceipt.insert(END, '插入包裹仿真数据成功！\n')
        root.update_idletasks()
        time.sleep(0.5)
        # ========================更改人员数量==============
        txtReceipt.insert(END, '设置人力资源数量为%s......\n' % person_res.get())
        update_person(cur, person_res.get(), run_arg)
        conn.commit()
        txtReceipt.insert(END, '人力资源设置完毕！\n')
        txtReceipt['state'] = DISABLED
        cur.close()
        conn.close()

        Flag['update_data'] += 1
        Flag['cost_of_item'] = 0


    def check_time(out_time):
        if isinstance(out_time, str):
            return out_time
        elif isinstance(out_time, bytes):
            return out_time.decode()


    def q_exit():
        if_exit = messagebox.askyesno("tkmessage", "要退出了，确定？")
        if if_exit > 0:
            root.destroy()
            return

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
    # # ============================资源配置=============================
    # # 标题
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
    # # ============================机器配置==========================
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
    for w_id in ConfigCheckBtn.WIG_ID:
        CHECK_BTN_ENTRY_DIC[w_id] = CheckBtnEntry(
            w_id, left_set_pad_center_left
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
        command=update_data
    ).grid(row=0, column=0)
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="启动仿真",
        command=run_sim
    ).grid(row=0, column=1)
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="存储数据",
        command=save_data
    ).grid(row=0, column=2)
    Button(
        master=right_output_pad_button,
        padx=btn_padx, pady=btn_pady, fg="black",
        font=('Times', font_btn, 'bold'),
        width=width_btn,
        text="退出",
        command=q_exit
    ).grid(row=0, column=3)
    # ========================================================
