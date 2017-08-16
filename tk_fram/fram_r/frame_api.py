from datetime import datetime
import time

from tkinter import END, NORMAL, DISABLED, Canvas, Scrollbar, Y, BOTH, Frame, \
    IntVar, Checkbutton
from tkinter import messagebox
from tkinter.messagebox import *

from tkinter.filedialog import askopenfilename

from .db_api import Mysql, insert_package, update_on_off, save_to_past_run, \
    read_result, update_person
# from simpy_lib import main
from .frame_r_view import Flag, ConfigFrame, CHECK_BTN_ENTRY_DIC, \
    LIST_VALUE_COMBOBOX, CURRENT_CANVAS_DICT, CURRENT_SHEET, \
    CACHE_BTN_ENTRY_DICT, CACHE_COMBOBOX_DICT, DAY_TIME_DICT
from .frame import CheckBtnEntryList


def save_data(package_num, date_plan, time_plan, root, txt_receipt):
    if not package_num.get():
        messagebox.showerror(
            "Tkinter-数据更新错误", "运行错误，请输入仿真件量！"
        )
        return
    if not date_plan.get():
        messagebox.showerror("Tkinter-数据更新错误",
                             "运行错误，请设置班次时间！")
        return
    if Flag['save_data'] > 0:
        messagebox.showerror("Tkinter-数据保存错误",
                             "数据已经保存，请勿重复操作！")
        return
    if Flag['run_sim'] == 0:
        messagebox.showerror("Tkinter-数据保存错误",
                             "运行错误，请先执行仿真！")
        return
    txt_receipt['state'] = NORMAL
    txt_receipt.insert(END, '*******************************\n')
    txt_receipt.insert(END, '开始储存数据......\n')
    root.update_idletasks()
    conn = Mysql().connect
    with conn as cur:
        save_to_past_run(cur)
    txt_receipt.insert(END,
                       '数据存储完毕！\n*******************************\n'
                       )
    txt_receipt['state'] = DISABLED
    Flag['save_data'] += 1


def run_sim(package_num, date_plan, time_plan, root, txt_receipt):
    """"""
    if not package_num.get():
        messagebox.showerror(
            "Tkinter-数据更新错误", "运行错误， 请输入仿真件量！"
        )
        return
    if not date_plan.get():
        messagebox.showerror("Tkinter-数据更新错误",
                             "运行错误，请设置班次时间！")
        return
    if Flag['update_data'] == 0:
        messagebox.showerror("Tkinter-仿真启动错误",
                             "运行错误，请先执行数据更新！")
        return
    if Flag['run_sim'] > 0:
        messagebox.showerror("Tkinter-仿真启动错误",
                             "仿真已经运行完成，请勿重复操作！")
        return
    run_arg = Flag['run_time']
    conn = Mysql().connect
    with conn as cur:
        cur.execute(
            "truncate o_machine_table;"
            "truncate o_pipeline_table;"
            "truncate o_truck_table"
        )

    txt_receipt['state'] = NORMAL
    txt_receipt.insert(END, '*******************************\n')
    txt_receipt.insert(END, '开始调用仿真函数......\n')
    root.update_idletasks()
    start_time = time.time()
    main(run_arg)
    run_time = '%.2f' % (time.time() - start_time)
    txt_receipt.insert(END, '仿真执行完毕\n')
    root.update_idletasks()
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
    txt_receipt['state'] = DISABLED
    root.update_idletasks()
    Flag['run_sim'] += 1
    Flag['save_data'] = 0


def update_data(package_num, date_plan, time_plan, root, txt_receipt):
    """"""
    for i in ConfigFrame.WIG_BTN_DICT[CURRENT_SHEET[0]]:
        CACHE_COMBOBOX_DICT[i] = CHECK_BTN_ENTRY_DIC[i].string_combobox.get()
    Flag['run_time'] = datetime.now()
    run_arg = Flag['run_time']
    if not package_num.get():
        messagebox.showerror(
            "Tkinter-数据更新错误", "运行错误，请输入仿真件量！")
        return
    if not date_plan.get():
        messagebox.showerror("Tkinter-数据更新错误",
                             "运行错误，请设置班次时间！")
        return

    # # #  显示结果
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
        update_on_off(cur, start_time, run_arg)

    txt_receipt.insert(END, '机器开关状态更新成功！\n')
    root.update_idletasks()
    time.sleep(0.5)
    # ======================== 插入测试数据=============
    txt_receipt.insert(END, '插入%s件包裹仿真数据......\n' % package_num.get())
    with conn as cur:
        insert_package(cur, package_num.get(), run_arg)
    txt_receipt.insert(END, '插入包裹仿真数据成功！\n')
    root.update_idletasks()
    time.sleep(0.5)
    # ========================更改人员数量==============
    txt_receipt.insert(END, '开始设置人力资源数量......\n')
    with conn as cur:
        update_person(cur, run_arg)
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
    if_exit = messagebox.askyesno("tkmessage", "要退出了，确定？")
    if if_exit > 0:
        root.destroy()
        return


def menu_file(root):
    askopenfilename()


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
    ConfigFrame.SHEET_LABEL_DICT[sheet].grid({'row': 0, 'column': column})
    if sheet == 'R':
        ConfigFrame.SHEET_VAR_DICT[sheet].set(1)
        ConfigFrame.SHEET_LABEL_DICT[sheet]['state'] = DISABLED
    return f'{sheet}标签初始化完成'


def switch_sheet(sheet: str, canvas_master):
    # 每次切换界面都会更新上一个界面的开关状态数据到 CACHE_BTN_ENTRY_DICT
    # 更新上一个界面的人数到 CACHE_COMBOBOX_DICT
    for i in ConfigFrame.WIG_BTN_DICT[CURRENT_SHEET[0]]:
        CACHE_BTN_ENTRY_DICT[i] = CHECK_BTN_ENTRY_DIC[i].var.get()
        CACHE_COMBOBOX_DICT[i] = CHECK_BTN_ENTRY_DIC[i].string_combobox.get()
    # ==============================================================
    sheet_btn = ConfigFrame.SHEET_LABEL_DICT[sheet]
    sheet_btn['state'] = DISABLED
    ConfigFrame.SHEET_VAR_DICT[CURRENT_SHEET[0]].set(0)
    ConfigFrame.SHEET_LABEL_DICT[CURRENT_SHEET[0]]['state'] = NORMAL
    CURRENT_CANVAS_DICT['canvas'].destroy()
    CURRENT_CANVAS_DICT['scrollbar'].destroy()
    CURRENT_CANVAS_DICT['canvas'], CURRENT_CANVAS_DICT['scrollbar'] = \
        create_canvas(canvas_master, sheet)
    # 更新当前选中标签至当前标签内存中
    CURRENT_SHEET[0] = sheet
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
    return (canvas_up, scrollbar_up)

def set_during_time(date_plan, time_plan):
    time_plan['values'] = DAY_TIME_DICT[date_plan.get()]

def clear_time(time_plan):
    time_plan.set('')