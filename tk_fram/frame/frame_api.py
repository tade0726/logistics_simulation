from datetime import datetime
import time

from tkinter import END, NORMAL, DISABLED, Canvas, Scrollbar, Y, BOTH, Frame, \
    IntVar, Checkbutton
from tkinter import messagebox
from tkinter.messagebox import *

from tkinter.filedialog import askopenfilename

from .db_api import Mysql, insert_package, update_on_off, save_to_past_run, \
    read_result, update_person, average_time, success_percent, discharge, csv_into_mysql
from .frame_view import Flag, ConfigFrame, CHECK_BTN_ENTRY_DIC, \
    LIST_VALUE_COMBOBOX, CURRENT, CACHE_INSTANCE_DICT, DAY_TIME_DICT, \
    NUM_TRANSLATE_DICT, R_J_DICT, ENTRY_STATUS_DIC
from .frame import CheckBtnEntryList, update_m_j

import xlrd


def save_data(root, txt_receipt):
    txt_receipt.insert(END, '*******************************\n')
    txt_receipt.insert(END, '开始储存数据......\n')
    root.update_idletasks()
    conn = Mysql().connect
    with conn as cur:
        save_to_past_run(cur)
    txt_receipt.insert(END,
                       '数据存储完毕！\n*******************************\n'
                       )
    root.update_idletasks()
    Flag['run_time'] = None


def run_sim(package_num, date_plan, time_plan, root, txt_receipt):
    """"""
    if Flag['update_data'] == 0:
        result = messagebox.askyesno("Tkmessage",
                                     "数据还未更新， 是否继续执行仿真")
        if result == 0:
            return
    if not package_num.get():
        messagebox.showerror(
            "Tkinter-数据更新错误", "运行错误， 请输入仿真件量！"
        )
        return
    if Flag['run_sim'] > 0:
        result = messagebox.askyesno("askyesno", "仿真已经运行完成，是否重新执行仿真")
        if result == 0:
            return
    conn = Mysql().connect
    Flag['run_time'] = Flag['run_time'] or datetime.now()
    run_arg = Flag['run_time']
    # ======================== 插入测试数据=============
    txt_receipt['state'] = NORMAL
    txt_receipt.insert(END, '插入%s件包裹仿真数据......\n' % package_num.get())
    root.update_idletasks()
    with conn as cur:
        insert_package(cur, package_num.get(), run_arg)
    txt_receipt.insert(END, '插入包裹仿真数据成功！\n')
    root.update_idletasks()
    time.sleep(0.5)

    with conn as cur:
        cur.execute(
            "truncate o_machine_table;"
            "truncate o_pipeline_table;"
            "truncate o_truck_table"
        )

    txt_receipt.insert(END, '*******************************\n')
    txt_receipt.insert(END, '开始调用仿真函数......\n')
    root.update_idletasks()
    start_time = time.time()
    # ================================
    from simpy_lib import main
    main(run_arg)
    run_time = '%.2f' % (time.time() - start_time)
    txt_receipt.insert(END, '仿真执行完毕\n')
    root.update_idletasks()
    time.sleep(0.5)
    txt_receipt.insert(END, '开始插入仿真数据......\n')
    root.update_idletasks()
    with conn as cur:
        csv_into_mysql(cur)
    txt_receipt.insert(END, '插入数据结束\n')
    root.update_idletasks()
    # ==============================================
    time.sleep(0.5)
    txt_receipt.insert(END, '开始读取仿真结果......\n')
    root.update_idletasks()
    time.sleep(0.5)
    root.update_idletasks()
    with conn as cur:
        result = read_result(cur)
    txt_receipt.insert(END, '*******************************\n')
    txt_receipt.insert(
        END, '最早到达时间:\t' + check_time(result['fast_time']) + '\n'
    )
    txt_receipt.insert(
        END, '最晚到达时间:\t' + check_time(result['later_time']) + '\n'
    )
    txt_receipt.insert(
        END,
        '最后一票处理时间:\t' + check_time(result['last_solve_time']) + '\n')
    txt_receipt.insert(
        END,
        '总处理时间(小时):\t' + '%.2f' % result['total_solve_time'] + '\n')
    txt_receipt.insert(
        END, '仿真运行时间(秒):\t' + check_time(run_time) + '\n')
    root.update_idletasks()
    txt_receipt.insert(END, '*******************************\n')
    txt_receipt.insert(END, '开始分析仿真结果......\n')
    root.update_idletasks()
    with conn as cur:
        average = average_time(cur)
    txt_receipt.insert(
        END,
        '票均时效(秒):\t' + '%.2f' % average + '\n'
    )
    root.update_idletasks()
    with conn as cur:
        percent = success_percent(cur)
    txt_receipt.insert(
        END,
        '时效达成率:\t' + '%.2f' % percent + '\n'
    )
    root.update_idletasks()
    with conn as cur:
        discharge_time = discharge(cur)
    txt_receipt.insert(
        END,
        '卸货等待时间(秒):\t' + '%.2f' % discharge_time + '\n'
    )
    save_data(root, txt_receipt)
    txt_receipt['state'] = DISABLED
    root.update_idletasks()
    Flag['run_sim'] += 1


def update_data(date_plan, time_plan, root, txt_receipt, final=True):
    """"""
    # 将当前界面所有控件的状态与人数保存到 CACHE_INSTANCE_DICT，防止更新时被忽略
    for i in ConfigFrame.WIG_BTN_DICT[CURRENT['SHEET']]:
        CACHE_INSTANCE_DICT[CURRENT['TIME']['start_time']][i]['status'] = \
            CHECK_BTN_ENTRY_DIC[i].var.get()
        if CURRENT['SHEET'] in NUM_TRANSLATE_DICT:
            CACHE_INSTANCE_DICT[CURRENT['TIME']['start_time']][i]['num'] = \
                int(CHECK_BTN_ENTRY_DIC[i].string_combobox.get()) / \
                NUM_TRANSLATE_DICT[CURRENT['SHEET']]
        else:
            CACHE_INSTANCE_DICT[CURRENT['TIME']['start_time']][i]['num'] = \
                CHECK_BTN_ENTRY_DIC[i].string_combobox.get()

    update_m_j()

    Flag['run_time'] = Flag['run_time'] or datetime.now()
    run_arg = Flag['run_time']
    if not date_plan.get():
        messagebox.showerror("Tkinter-数据更新错误",
                             "运行错误，请选择日期与时段！")
        return

    # # #  显示结果
    if final:
        txt_receipt['state'] = NORMAL
    txt_receipt.delete('1.0', END)
    root.update_idletasks()
    # ========================更改开关状态==============
    txt_receipt.insert(END, '机器开关状态更新......\n')
    day = date_plan.get()
    start, end = time_plan.get().split('-')
    start_time = day + ' ' + start
    conn = Mysql().connect
    with conn as cur:
        for time, value in CACHE_INSTANCE_DICT.items():
            update_on_off(cur, time, value, run_arg)

    txt_receipt.insert(END, '机器开关状态更新成功！\n')
    root.update_idletasks()
    # ========================更改人员数量==============
    txt_receipt.insert(END, '开始设置人力资源数量......\n')
    with conn as cur:
        for time, value in CACHE_INSTANCE_DICT.items():
            update_person(cur, time, value, run_arg)
    txt_receipt.insert(END, '人力资源设置完毕！\n')
    txt_receipt['state'] = DISABLED

    Flag['update_data'] += 1
    Flag['run_sim'] = 0


def check_time(out_time):
    if isinstance(out_time, str):
        return out_time
    elif isinstance(out_time, bytes):
        return out_time.decode()


def q_exit(root):
    if_exit = messagebox.askyesno("Tkmessage", "要退出了，确定？")
    if if_exit > 0:
        root.destroy()
        return


def menu_file(root):
    filename = askopenfilename()
    try:
        data = xlrd.open_workbook(filename)
        for sheet in ConfigFrame.SHEET_LIST:
            table = data.sheet_by_name(sheet)
            for row in range(table.nrows)[1:]:
                column = 1
                for key in table.row_values(0)[1:]:
                    w_id = table.row_values(row)[0]
                    value = table.row_values(row)[column]
                    CACHE_INSTANCE_DICT[w_id][key] = int(value)
                    column += 1
        for w_id in ConfigFrame.WIG_BTN_DICT[CURRENT['SHEET']]:
            CHECK_BTN_ENTRY_DIC[w_id].init_on_off_status()

        update_m_j()
    except FileNotFoundError:
        pass

def init_sheet(master, canvas_master):
    column = 0
    for sheet in ConfigFrame.SHEET_LIST:
        yield create_sheet(master, sheet, column, canvas_master)
        column += 1


def create_sheet(master, sheet: str, column: int, canvas_master):
    ConfigFrame.SHEET_VAR_DICT[sheet] = IntVar()
    ConfigFrame.SHEET_LABEL_DICT[sheet] = Checkbutton(
        master=master,
        variable=ConfigFrame.SHEET_VAR_DICT[sheet],
        command=lambda: switch_sheet(sheet, canvas_master)
    )
    ConfigFrame.SHEET_LABEL_DICT[sheet].config(
        ConfigFrame.SHEET_ATTR_DICT[sheet])
    ConfigFrame.SHEET_LABEL_DICT[sheet].grid(
        {'row': 0, 'column': column, 'sticky': 'nswe'}
    )
    if sheet == 'R':
        ConfigFrame.SHEET_VAR_DICT[sheet].set(1)
        ConfigFrame.SHEET_LABEL_DICT[sheet]['state'] = DISABLED
    return


def switch_sheet(sheet: str, canvas_master):
    # 每次切换界面都会更新上一个界面的开关状态数据到 CACHE_BTN_ENTRY_DICT
    # 更新上一个界面的人数到 CACHE_COMBOBOX_DICT
    for i in ConfigFrame.WIG_BTN_DICT[CURRENT['SHEET']]:
        CACHE_INSTANCE_DICT[CURRENT['TIME']['start_time']][i]['status'] = \
            CHECK_BTN_ENTRY_DIC[i].var.get()
        if CURRENT['SHEET'] in NUM_TRANSLATE_DICT:
            CACHE_INSTANCE_DICT[CURRENT['TIME']['start_time']][i]['num'] = \
                int(CHECK_BTN_ENTRY_DIC[i].string_combobox.get() / \
                NUM_TRANSLATE_DICT[CURRENT['SHEET']])
        else:
            CACHE_INSTANCE_DICT[CURRENT['TIME']['start_time']][i]['num'] = \
                CHECK_BTN_ENTRY_DIC[i].string_combobox.get()
    # ==============================================================
    sheet_btn = ConfigFrame.SHEET_LABEL_DICT[sheet]
    sheet_btn['state'] = DISABLED
    ConfigFrame.SHEET_VAR_DICT[CURRENT['SHEET']].set(0)
    ConfigFrame.SHEET_LABEL_DICT[CURRENT['SHEET']]['state'] = NORMAL
    CURRENT['CANVAS_DICT']['canvas'].destroy()
    CURRENT['CANVAS_DICT']['scrollbar'].destroy()
    CURRENT['CANVAS_DICT']['canvas'], CURRENT['CANVAS_DICT']['scrollbar'] = \
        create_canvas(canvas_master, sheet)
    # 更新当前选中标签至当前标签内存中
    CURRENT['SHEET'] = sheet
    return


def create_canvas(master, sheet: str):
    canvas_up = Canvas(master)
    scrollbar_up = Scrollbar(master)
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
    # 
    frame_up = Frame(canvas_up, width=50, height=100)
    frame_up.pack(side="top", fill=BOTH)
    canvas_up.create_window(0, 0, window=frame_up, anchor="nw")

    bas_up = [0, 0, 0, 50]
    for w_id in ConfigFrame.WIG_BTN_DICT[sheet]:
        CHECK_BTN_ENTRY_DIC[w_id] = CheckBtnEntryList(
            w_id,
            frame_up,
            LIST_VALUE_COMBOBOX[sheet]
        )
        CHECK_BTN_ENTRY_DIC[w_id].init_on_off_status()
        canvas_up["scrollregion"] = "%d %d %d %d" % (
            bas_up[0],
            bas_up[1],
            bas_up[2],
            bas_up[3]
        )
        bas_up[3] += 50/3
    # if sheet == 'J':
    #     did_set = set()
    #     for key, value in R_J_DICT.items():
    #         if value not in did_set:
    #             j_status_list = []
    #             for j_id in value:
    #                 if CHECK_BTN_ENTRY_DIC[j_id].var.get() == 1:
    #                     j_status_list.append(j_id)
    #             if len(j_status_list) == 1:
    #                 CHECK_BTN_ENTRY_DIC[j_status_list[0]].check_btn[
    #                     'state'] = DISABLED
    #             did_set.add(value)

    return (canvas_up, scrollbar_up)

def update_time_date(date_plan, time_plan):
    day = date_plan.get()
    period = time_plan.get()
    start_time = day + ' ' + period.split('-')[0]
    CURRENT['TIME']['start_time'] = start_time
    for i in ConfigFrame.WIG_BTN_DICT[CURRENT['SHEET']]:
        CACHE_INSTANCE_DICT[CURRENT['TIME']['start_time']][i]['num'] /= 2
        CHECK_BTN_ENTRY_DIC[i].init_on_off_status()
        # if i == 'j41_1' or 'h' in i:
        #     CHECK_BTN_ENTRY_DIC[i].var.set(
        #         1
        #     )
        # else:
        #     CHECK_BTN_ENTRY_DIC[i].var.set(
        #         CACHE_INSTANCE_DICT[start_time][i]['status']
        #     )
        #
        #
        # CHECK_BTN_ENTRY_DIC[i].string.set(
        #     ENTRY_STATUS_DIC[CHECK_BTN_ENTRY_DIC[i].var.get()]
        # )
        # CHECK_BTN_ENTRY_DIC[i].change_color(CHECK_BTN_ENTRY_DIC[i].entry)
        # CHECK_BTN_ENTRY_DIC[i].string_combobox.set(
        #     CACHE_INSTANCE_DICT[start_time][i]['num']
        # )
        # CHECK_BTN_ENTRY_DIC[i].change_combobox_status(CHECK_BTN_ENTRY_DIC[i])

def update_to_cache():
    for key, value in CHECK_BTN_ENTRY_DIC.items():
        CACHE_INSTANCE_DICT[CURRENT['TIME']['start_time']][key]['status'] = \
            value.var.get()
        CACHE_INSTANCE_DICT[CURRENT['TIME']['start_time']][key]['num'] = \
            value.string_combobox.get()


def set_during_time(date_plan, time_plan):
    time_plan.set('')
    time_plan['values'] = DAY_TIME_DICT[date_plan.get()]