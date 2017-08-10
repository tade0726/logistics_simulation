from datetime import datetime
import time

from tkinter import END, NORMAL, DISABLED
from tkinter import messagebox

from .db_api import Mysql, insert_package, update_on_off, save_to_past_run, \
    read_result, update_person
from simpy_lib import main
from .frame_r_view import Flag


def save_data(package_num, person_res, root, txtReceipt):
    if not package_num.get():
        messagebox.showerror("Tkinter-数据更新错误", "运行错误，请输入仿真件量！")
        return
    if not person_res.get():
        messagebox.showerror("Tkinter-数据更新错误",
                             "运行错误，请输入初分拣区卸货口人数！")
        return
    if Flag['save_data'] > 0:
        messagebox.showerror("Tkinter-数据保存错误",
                             "数据已经保存，请勿重复操作！")
        return
    if Flag['run_sim'] == 0:
        messagebox.showerror("Tkinter-数据保存错误",
                             "运行错误，请先执行仿真！")
        return
    txtReceipt['state'] = NORMAL
    txtReceipt.insert(END, '*******************************\n')
    txtReceipt.insert(END, '开始储存数据......\n')
    root.update_idletasks()
    conn = Mysql().connect
    with conn as cur:
        save_to_past_run(cur)
    txtReceipt.insert(END, '数据存储完毕！\n'
                           '*******************************\n')
    txtReceipt['state'] = DISABLED
    Flag['save_data'] += 1


def run_sim(package_num, person_res, root, txtReceipt):
    """"""
    if not package_num.get():
        messagebox.showerror("Tkinter-数据更新错误", "运行错误， 请输入仿真件量！")
        return
    if not person_res.get():
        messagebox.showerror("Tkinter-数据更新错误",
                             "运行错误，请输入初分拣区卸货口人数！")
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
    with conn as cur:
        result = read_result(cur)
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
    Flag['run_sim'] += 1
    Flag['save_data'] = 0


def update_data(package_num, person_res, root, txtReceipt):
    """"""
    Flag['run_time'] = datetime.now()
    run_arg = Flag['run_time']
    if not package_num.get():
        messagebox.showerror("Tkinter-数据更新错误", "运行错误，请输入仿真件量！")
        return
    if not person_res.get():
        messagebox.showerror("Tkinter-数据更新错误",
                             "运行错误，请输入初分拣区卸货口人数！")
        return

    # # #  显示结果
    txtReceipt['state'] = NORMAL
    txtReceipt.delete('1.0', END)
    root.update_idletasks()
    # ========================更改开关状态==============
    txtReceipt.insert(END, '机器开关状态更新......\n')
    conn = Mysql().connect
    with conn as cur:
        update_on_off(cur, run_arg)

    txtReceipt.insert(END, '机器开关状态更新成功！\n')
    root.update_idletasks()
    time.sleep(0.5)
    # ======================== 插入测试数据=============
    txtReceipt.insert(END, '插入%s件包裹仿真数据......\n' % package_num.get())
    with conn as cur:
        insert_package(cur, package_num.get(), run_arg)
    txtReceipt.insert(END, '插入包裹仿真数据成功！\n')
    root.update_idletasks()
    time.sleep(0.5)
    # ========================更改人员数量==============
    txtReceipt.insert(END, '设置人力资源数量为%s......\n' % person_res.get())
    with conn as cur:
        update_person(cur, person_res.get(), run_arg)
    txtReceipt.insert(END, '人力资源设置完毕！\n')
    txtReceipt['state'] = DISABLED

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