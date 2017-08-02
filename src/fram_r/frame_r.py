# -*- coding: utf-8 -*-

from src.fram_r import App, CheckBtnCreate, EntryCreate
from src.fram_r import messagebox
from src.fram_r.frame_r_view import *

import pymysql


def init_app(master, wig):
    """"""
    return App(master=master,
               pack=ConfigApp.RELOAD_FRAME[wig]['pack'],
               attr=ConfigApp.RELOAD_FRAME[wig]['attr'])

def init_check_btn(master, id, var, command):
    """"""
    return CheckBtnCreate(
        master=master,
        grid_dic=ConfigCheckBtn.R_CHECK_BTN[id]['grid'],
        attr_dic=ConfigCheckBtn.R_CHECK_BTN[id]['attr'],
        id=id,
        var=var,
        command=command
    )

def init_btn_entry_val_from_sql():
    """"""
    var_dic = {}
    conn = pymysql.connect(host=DATABASES['HOST'],
                           user=DATABASES['USER'],
                           passwd=DATABASES['PASSWORD'],
                           db=DATABASES['NAME'])
    cur = conn.cursor()
    cur.execute("select equipment_port, equipment_status from i_equipment_io "
                "where equipment_id like 'r%'")
    result = cur.fetchall()
    for item in result:
        var_dic[item[0]] = item[1]
    cur.close()
    conn.close()
    return var_dic


def init_entry(master, id, text_var):
    """
    
    :param master: 
    :param id: 
    :param var: 
    :return: 
    """
    return EntryCreate(
        master=master,
        attr_dic=ConfigCheckBtn.R_ENTRY[id]['attr'],
        grid_dic=ConfigCheckBtn.R_ENTRY[id]['grid'],
        text_var=text_var
    )


def init_r_frame(root: Tk):
    """"""
    #  ===================顶部标题面板================
    top = init_app(
        master=root, wig='TOP_FRAME')
    #  =================左侧设置基底面板===============
    left = init_app(
        master=root, wig='LEFT_FRAME')
    #  =================右侧输出基底面板===============
    right = init_app(
        master=root,
        wig='RIGHT_FRAME')
    #  =============================================

    #  ================左侧包裹数，人力资源数 ==========
    left_set_pad_package = init_app(
        master=left,
        wig='LEFT_SET_PAD_TOP_PACKAGE'
    )
    #  ===============右侧输出标题样式=================
    right_output_pad_title = init_app(
        master=right,
        wig='RIGHT_TITLE'
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
    #  ==============右侧中部输出面板样式===============
    right_output_pad_info = init_app(
        master=right,
        wig='RIGHT_OUTPUT_PAD_INFO')
    #  =============右侧下部按钮控件样式================
    right_output_pad_button = init_app(
        master=right,
        wig='RIGHT_BUTTON')
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()
    var7 = IntVar()
    var8 = IntVar()
    var9 = IntVar()
    var10 = IntVar()
    var11 = IntVar()
    var12 = IntVar()
    var13 = IntVar()
    var14 = IntVar()
    var15 = IntVar()
    var16 = IntVar()
    var17 = IntVar()
    var18 = IntVar()
    var19 = IntVar()
    var20 = IntVar()
    var21 = IntVar()
    var22 = IntVar()
    var23 = IntVar()
    var24 = IntVar()
    var25 = IntVar()
    var26 = IntVar()
    var27 = IntVar()
    var28 = IntVar()
    var29 = IntVar()
    var30 = IntVar()
    var31 = IntVar()
    var32 = IntVar()

    e_r1 = StringVar()
    e_r2 = StringVar()
    e_r3 = StringVar()
    e_r4 = StringVar()
    e_r5 = StringVar()
    e_r6 = StringVar()
    e_r7 = StringVar()
    e_r8 = StringVar()
    e_r9 = StringVar()
    e_r10 = StringVar()
    e_r11 = StringVar()
    e_r12 = StringVar()
    e_r13 = StringVar()
    e_r14 = StringVar()
    e_r15 = StringVar()
    e_r16 = StringVar()
    e_r17 = StringVar()
    e_r18 = StringVar()
    e_r19 = StringVar()
    e_r20 = StringVar()
    e_r21 = StringVar()
    e_r22 = StringVar()
    e_r23 = StringVar()
    e_r24 = StringVar()
    e_r25 = StringVar()
    e_r26 = StringVar()
    e_r27 = StringVar()
    e_r28 = StringVar()
    e_r29 = StringVar()
    e_r30 = StringVar()
    e_r31 = StringVar()
    e_r32 = StringVar()

    # e_r1.set('关机')
    # e_r2.set('关机')
    # e_r3.set('关机')
    # e_r4.set('关机')
    # e_r5.set('关机')
    # e_r6.set('关机')
    # e_r7.set('关机')
    # e_r8.set('关机')
    # e_r9.set('关机')
    # e_r10.set('关机')
    # e_r11.set('关机')
    # e_r12.set('关机')
    # e_r13.set('关机')
    # e_r14.set('关机')
    # e_r15.set('关机')
    # e_r16.set('关机')
    # e_r17.set('关机')
    # e_r18.set('关机')
    # e_r19.set('关机')
    # e_r20.set('关机')
    # e_r21.set('关机')
    # e_r22.set('关机')
    # e_r23.set('关机')
    # e_r24.set('关机')
    # e_r25.set('关机')
    # e_r26.set('关机')
    # e_r27.set('关机')
    # e_r28.set('关机')
    # e_r29.set('关机')
    # e_r30.set('关机')
    # e_r31.set('关机')
    # e_r32.set('关机')

    def cost_of_item():
        """"""
        on_off_dict = {}
        on_off_dict['r1_1'] = r1_1.var.get()
        on_off_dict['r1_2'] = r1_2.var.get()
        on_off_dict['r1_3'] = r1_3.var.get()
        on_off_dict['r1_4'] = r1_4.var.get()
        # on_off_dict['r2_1'] = r2_1.var.get()
        # on_off_dict['r2_2'] = r2_2.var.get()
        # on_off_dict['r2_3'] = r2_3.var.get()
        # on_off_dict['r2_4'] = r2_4.var.get()
        # on_off_dict['r3_1'] = r3_1.var.get()
        # on_off_dict['r3_2'] = r3_2.var.get()
        # on_off_dict['r3_3'] = r3_3.var.get()
        # on_off_dict['r3_4'] = r3_4.var.get()
        # on_off_dict['r4_1'] = r4_1.var.get()
        # on_off_dict['r4_2'] = r4_2.var.get()
        # on_off_dict['r4_3'] = r4_3.var.get()
        # on_off_dict['r4_4'] = r4_4.var.get()
        # on_off_dict['r5_1'] = r5_1.var.get()
        # on_off_dict['r5_2'] = r5_2.var.get()
        # on_off_dict['r5_3'] = r5_3.var.get()
        # on_off_dict['r5_4'] = r5_4.var.get()

        conn = pymysql.connect(host=DATABASES['HOST'],
                               user=DATABASES['USER'],
                               passwd=DATABASES['PASSWORD'],
                               db=DATABASES['NAME'])
        cur = conn.cursor()

        # 更改开关状态
        update_on_off(cur, on_off_dict)
        conn.commit()

        # 插入测试数据
        insert_package(cur, package_num.get())
        conn.commit()

        # 更改人员数量
        update_person(cur, person_res.get())
        conn.commit()

        result = read_result(cur)

        cur.close()
        conn.close()

        # #  显示结果
        txtReceipt['state'] = NORMAL
        txtReceipt.delete('1.0', END)
        txtReceipt.insert(END, '最早到达时间:\t\t\t' + result['fast_time'] + '\n')
        txtReceipt.insert(END, '最晚到达时间:\t\t\t' + result['later_time'] + '\n')
        txtReceipt.insert(END, '最后一票处理时间:\t\t\t' + result['last_solve_time']
                          + '\n')
        txtReceipt.insert(END, '总处理时间:\t\t\t' + result['total_solve_time'] +
                          '\n')
        txtReceipt['state'] = DISABLED

    def chk_button_value(var, e_r):
        """"""
        e_r.set(status_dict[var.get()])

    def update_on_off(cursor, data: dict):
        # equipment_port 需要确定
        for item in data.items():
            cursor.execute(
                "update i_equipment_io set equipment_status=%s where "
                "equipment_port=%s" % (item[1], item[0])
            )

    def insert_package(cursor, num: str):
        cursor.execute("truncate i_od_parcel_landside")
        cursor.execute("insert into i_od_parcel_landside select * from "
                       "i_od_parcel_landside_all limit %s" % num)

    def update_person(cursor, num: str):
        # 需要指定 resource_id 范围
        cursor.execute("update i_resource_limit set resouce_limit={} where "
                       "resource_id like 'man_m%' ".format(num))

    def read_result(cursor):
        cursor.execute("select run_time from o_machine_table order by run_time "
                       "desc limit 1")
        run_time = cursor.fetchone()[0]
        cursor.execute(
            "select min(cast(real_time_stamp as datetime)), "
            "max(cast(real_time_stamp as datetime)) from o_machine_table where "
            "action='wait' and run_Time='{}' and equipment_id like 'r%'".format(
                run_time))

        fast_time, later_time = cursor.fetchone()
        cursor.execute(
            "select max(cast(real_time_stamp as datetime)), "
            "(max(time_stamp)-min(time_stamp))/3600 from o_machine_table where "
            "action='wait' and run_Time='{}'".format(run_time))
        last_solve_time, total_solve_time = cursor.fetchone()
        return {
            'fast_time': fast_time,
            'later_time': later_time,
            'last_solve_time': last_solve_time,
            'total_solve_time': total_solve_time
        }

    def q_exit():
        if_exit = messagebox.askyesno("tkmessage", "要退出了，确定？")
        if if_exit > 0:
            root.destroy()
            return

    # ==============================Heading===========================
    lbl_info = Label(top,
                     font=('arial', 18, 'bold'),
                     text='\t\t\t\t杭州分拣中心仿真系统\t\t\t\t',
                     bd=8,
                     # width=59,
                     anchor='w')
    lbl_info.grid(row=0, column=0)
    # ============================包裹设置参数========================
    lbl_package = Label(
        master=left_set_pad_package,
        font=('arial', 12),
        text='快件数量',
        bd=2,
        anchor='w'
    )
    lbl_package.grid(row=0, column=0)
    package_num = Entry(
        master=left_set_pad_package,
        width=35
    )
    package_num.grid(row=0, column=1)
    # ============================资源配置=============================
    # 标题
    lbl_resource = Label(
        master=left_set_pad_package,
        font=('arial', 12),
        text='人力资源数：',
        bd=2,
        anchor='w'
    )
    lbl_resource.grid(row=0, column=2)
    # 选择人数
    person_res = Spinbox(
        master=left_set_pad_package,
        width=35,
        values=(1, 2))
    person_res.grid(row=0, column=3)
    # ============================机器配置==========================
    # 路侧卸货标题-L2L
    lbl_unload = Label(
        master=left_set_pad_center_left,
        font=(
            'arial',
            10,
            # 'bold'
        ),
        relief='raise',
        text='L2L卸货区',
        bd=4,
        anchor='w'
    )
    lbl_unload.grid(row=0, column=0)
    # 路侧卸货标题-L2L,L2A,L2S2A,L2S2L
    lbl_unload = Label(
        master=left_set_pad_center_right,
        font=(
            'arial',
            10,
            # 'bold'
        ),
        relief='raise',
        text='L2L,L2A,L2S卸货区',
        bd=4,
        anchor='w'
    )
    lbl_unload.grid(row=0, column=3)

    # ###################     卸货区数据      =====================
    status_dict = {0: '关机', 1: '开机'}
    btn_entry_dict = init_btn_entry_val_from_sql()
    # ===================     R1卸货区       =====================
    r1_1 = init_check_btn(
        master=left_set_pad_center_left, id='r1_1', var=var1,
        command=lambda: chk_button_value(var1, e_r1))
    txt_r1_1 = init_entry(
        master=left_set_pad_center_left, id='r1_1', text_var=e_r1)
    r1_1.var.set(btn_entry_dict['r1_1'])
    e_r1.set(status_dict[r1_1.var.get()])
    r1_2 = init_check_btn(
        master=left_set_pad_center_left, id='r1_2', var=var2,
        command=lambda: chk_button_value(var2, e_r2))
    txt_r1_2 = init_entry(
        master=left_set_pad_center_left, id='r1_2', text_var=e_r2)
    r1_2.var.set(btn_entry_dict['r1_2'])
    e_r2.set(status_dict[r1_2.var.get()])
    r1_3 = init_check_btn(
        master=left_set_pad_center_left, id='r1_3', var=var3,
        command=lambda: chk_button_value(var3, e_r3))
    txt_r1_3 = init_entry(
        master=left_set_pad_center_left, id = 'r1_3', text_var=e_r3)
    r1_3.var.set(btn_entry_dict['r1_3'])
    e_r3.set(status_dict[r1_3.var.get()])
    r1_4 = init_check_btn(
        master=left_set_pad_center_left, id='r1_4', var=var4,
        command=lambda: chk_button_value(var4, e_r4))
    txt_r1_4 = init_entry(
        master=left_set_pad_center_left, id='r1_4', text_var=e_r4)
    r1_4.var.set(btn_entry_dict['r1_4'])
    e_r4.set(status_dict[r1_4.var.get()])

    # =====================    R2卸货区       =====================
    r2_1 = init_check_btn(
        master=left_set_pad_center_left, id='r2_1', var=var5,
        command=lambda: chk_button_value(var5, e_r5))
    txt_r2_1 = init_entry(
        master=left_set_pad_center_left, id='r2_1', text_var=e_r5)
    r2_1.var.set(btn_entry_dict['r2_1'])
    e_r5.set(status_dict[r2_1.var.get()])
    r2_2 = init_check_btn(
        master=left_set_pad_center_left, id='r2_2', var=var6,
        command=lambda: chk_button_value(var6, e_r6))
    txt_r2_2 = init_entry(
        master=left_set_pad_center_left, id='r2_2', text_var=e_r6)
    r2_2.var.set(btn_entry_dict['r2_2'])
    e_r6.set(status_dict[r2_2.var.get()])
    r2_3 = init_check_btn(
        master=left_set_pad_center_left, id='r2_3', var=var7,
        command=lambda: chk_button_value(var7, e_r7))
    txt_r2_3 = init_entry(
        master=left_set_pad_center_left, id='r2_3', text_var=e_r7)
    r2_3.var.set(btn_entry_dict['r2_3'])
    e_r7.set(status_dict[r2_3.var.get()])
    r2_4 = init_check_btn(
        master=left_set_pad_center_left, id='r2_4', var=var8,
        command=lambda: chk_button_value(var8, e_r8))
    txt_r2_4 = init_entry(
        master=left_set_pad_center_left, id='r2_4', text_var=e_r8)
    r2_4.var.set(btn_entry_dict['r2_4'])
    e_r8.set(status_dict[r2_4.var.get()])

    # =======================    R3卸货区     =======================
    r3_1 = init_check_btn(
        master=left_set_pad_center_right, id='r3_1', var=var9,
        command=lambda: chk_button_value(var9, e_r9))
    txt_r3_1 = init_entry(
        master=left_set_pad_center_right, id='r3_1', text_var=e_r9)
    r3_1.var.set(btn_entry_dict['r3_1'])
    e_r9.set(status_dict[r3_1.var.get()])
    r3_2 = init_check_btn(
        master=left_set_pad_center_right, id='r3_2', var=var10,
        command=lambda: chk_button_value(var10, e_r10))
    txt_r3_2 = init_entry(
        master=left_set_pad_center_right, id='r3_2', text_var=e_r10)
    r3_2.var.set(btn_entry_dict['r3_2'])
    e_r10.set(status_dict[r3_2.var.get()])
    r3_3 = init_check_btn(
        master=left_set_pad_center_right, id='r3_3', var=var11,
        command=lambda: chk_button_value(var11, e_r11))
    txt_r3_3 = init_entry(
        master=left_set_pad_center_right, id='r3_3', text_var=e_r11)
    r3_3.var.set(btn_entry_dict['r3_3'])
    e_r11.set(status_dict[r3_3.var.get()])
    r3_4 = init_check_btn(
        master=left_set_pad_center_right, id='r3_4', var=var12,
        command=lambda: chk_button_value(var12, e_r12))
    txt_r3_4 = init_entry(
        master=left_set_pad_center_right, id='r3_4', text_var=e_r12)
    r3_4.var.set(btn_entry_dict['r3_4'])
    e_r12.set(status_dict[r3_4.var.get()])
    r3_5 = init_check_btn(
        master=left_set_pad_center_right, id='r3_5', var=var13,
        command=lambda: chk_button_value(var13, e_r13))
    txt_r3_5 = init_entry(
        master=left_set_pad_center_right, id='r3_5', text_var=e_r13)
    r3_5.var.set(btn_entry_dict['r3_5'])
    e_r13.set(status_dict[r3_5.var.get()])
    r3_6 = init_check_btn(
        master=left_set_pad_center_right, id='r3_6', var=var14,
        command=lambda: chk_button_value(var14, e_r14))
    txt_r3_6 = init_entry(
        master=left_set_pad_center_right, id='r3_6', text_var=e_r14)
    r3_6.var.set(btn_entry_dict['r3_6'])
    e_r14.set(status_dict[r3_6.var.get()])
    r3_7 = init_check_btn(
        master=left_set_pad_center_right, id='r3_7', var=var15,
        command=lambda: chk_button_value(var15, e_r15))
    txt_r3_7 = init_entry(
        master=left_set_pad_center_right, id='r3_7', text_var=e_r15)
    r3_7.var.set(btn_entry_dict['r3_7'])
    e_r15.set(status_dict[r3_7.var.get()])
    r3_8 = init_check_btn(
        master=left_set_pad_center_right, id='r3_8', var=var16,
        command=lambda: chk_button_value(var16, e_r16))
    txt_r3_8 = init_entry(
        master=left_set_pad_center_right, id='r3_8', text_var=e_r16)
    r3_8.var.set(btn_entry_dict['r3_8'])
    e_r16.set(status_dict[r3_8.var.get()])
    r3_9 = init_check_btn(
        master=left_set_pad_center_right, id='r3_9', var=var17,
        command=lambda: chk_button_value(var17, e_r17))
    txt_r3_9 = init_entry(
        master=left_set_pad_center_right, id='r3_9', text_var=e_r17)
    r3_9.var.set(btn_entry_dict['r3_9'])
    e_r17.set(status_dict[r3_9.var.get()])
    r3_10 = init_check_btn(
        master=left_set_pad_center_right, id='r3_10', var=var18,
        command=lambda: chk_button_value(var18, e_r18))
    txt_r3_10 = init_entry(
        master=left_set_pad_center_right, id='r3_10', text_var=e_r18)
    r3_10.var.set(btn_entry_dict['r3_10'])
    e_r18.set(status_dict[r3_10.var.get()])

    # ===========================R4卸货区==============================
    r4_1 = init_check_btn(
        master=left_set_pad_center_right, id='r4_1', var=var19,
        command=lambda: chk_button_value(var19, e_r19))
    txt_r4_1 = init_entry(
        master=left_set_pad_center_right, id='r4_1', text_var=e_r19)
    r4_1.var.set(btn_entry_dict['r4_1'])
    e_r19.set(status_dict[r4_1.var.get()])
    r4_2 = init_check_btn(
        master=left_set_pad_center_right, id='r4_2', var=var20,
        command=lambda: chk_button_value(var20, e_r20))
    txt_r4_2 = init_entry(
        master=left_set_pad_center_right, id='r4_2', text_var=e_r20)
    r4_2.var.set(btn_entry_dict['r4_2'])
    e_r20.set(status_dict[r4_2.var.get()])
    r4_3 = init_check_btn(
        master=left_set_pad_center_right, id='r4_3', var=var21,
        command=lambda: chk_button_value(var21, e_r21))
    txt_r4_3 = init_entry(
        master=left_set_pad_center_right, id='r4_3', text_var=e_r21)
    r4_3.var.set(btn_entry_dict['r4_3'])
    e_r21.set(status_dict[r4_3.var.get()])
    r4_4 = init_check_btn(
        master=left_set_pad_center_right, id='r4_4', var=var22,
        command=lambda: chk_button_value(var22, e_r22))
    txt_r4_4 = init_entry(
        master=left_set_pad_center_right, id='r4_4', text_var=e_r22)
    r4_4.var.set(btn_entry_dict['r4_4'])
    e_r22.set(status_dict[r4_4.var.get()])
    r4_5 = init_check_btn(
        master=left_set_pad_center_right, id='r4_5', var=var23,
        command=lambda: chk_button_value(var23, e_r23))
    txt_r4_5 = init_entry(
        master=left_set_pad_center_right, id='r4_5', text_var=e_r23)
    r4_5.var.set(btn_entry_dict['r4_5'])
    e_r23.set(status_dict[r4_5.var.get()])
    r4_6 = init_check_btn(
        master=left_set_pad_center_right, id='r4_6', var=var24,
        command=lambda: chk_button_value(var24, e_r24))
    txt_r4_6 = init_entry(
        master=left_set_pad_center_right, id='r4_6', text_var=e_r24)
    r4_6.var.set(btn_entry_dict['r4_6'])
    e_r24.set(status_dict[r4_6.var.get()])
    r4_7 = init_check_btn(
        master=left_set_pad_center_right, id='r4_7', var=var25,
        command=lambda: chk_button_value(var25, e_r25))
    txt_r4_7 = init_entry(
        master=left_set_pad_center_right, id='r4_7', text_var=e_r25)
    r4_7.var.set(btn_entry_dict['r4_7'])
    e_r25.set(status_dict[r4_7.var.get()])
    r4_8 = init_check_btn(
        master=left_set_pad_center_right, id='r4_8', var=var26,
        command=lambda: chk_button_value(var26, e_r26))
    txt_r4_8 = init_entry(
        master=left_set_pad_center_right, id='r4_8', text_var=e_r26)
    r4_8.var.set(btn_entry_dict['r4_8'])
    e_r26.set(status_dict[r4_8.var.get()])
    r4_9 = init_check_btn(
        master=left_set_pad_center_right, id='r4_9', var=var27,
        command=lambda: chk_button_value(var27, e_r27))
    txt_r4_9 = init_entry(
        master=left_set_pad_center_right, id='r4_9', text_var=e_r27)
    r4_9.var.set(btn_entry_dict['r4_9'])
    e_r27.set(status_dict[r4_9.var.get()])
    r4_10 = init_check_btn(
        master=left_set_pad_center_right, id='r4_10', var=var28,
        command=lambda: chk_button_value(var28, e_r28))
    txt_r4_10 = init_entry(
        master=left_set_pad_center_right, id='r4_10', text_var=e_r28)
    r4_10.var.set(btn_entry_dict['r4_10'])
    e_r28.set(status_dict[r4_10.var.get()])

    # # ======================== R5 卸货区 ============================
    r5_1 = init_check_btn(
        master=left_set_pad_center_right, id='r5_1', var=var29,
        command=lambda: chk_button_value(var29, e_r29))
    txt_r5_1 = init_entry(
        master=left_set_pad_center_right, id='r5_1', text_var=e_r29)
    r5_1.var.set(btn_entry_dict['r5_1'])
    e_r29.set(status_dict[r5_1.var.get()])
    r5_2 = init_check_btn(
        master=left_set_pad_center_right, id='r5_2', var=var30,
        command=lambda: chk_button_value(var30, e_r30))
    txt_r5_2 = init_entry(
        master=left_set_pad_center_right, id='r5_2', text_var=e_r30)
    r5_2.var.set(btn_entry_dict['r5_2'])
    e_r30.set(status_dict[r5_2.var.get()])
    r5_3 = init_check_btn(
        master=left_set_pad_center_right, id='r5_3', var=var31,
        command=lambda: chk_button_value(var31, e_r31))
    txt_r5_3 = init_entry(
        master=left_set_pad_center_right, id='r5_3', text_var=e_r31)
    r5_3.var.set(btn_entry_dict['r5_3'])
    e_r31.set(status_dict[r5_3.var.get()])
    r5_4 = init_check_btn(
        master=left_set_pad_center_right, id='r5_4', var=var32,
        command=lambda: chk_button_value(var32, e_r32))
    txt_r5_4 = init_entry(
        master=left_set_pad_center_right, id='r5_4', text_var=e_r32)
    r5_4.var.set(btn_entry_dict['r5_4'])
    e_r32.set(status_dict[r5_4.var.get()])

    # ============================仿真结果输出面板======================
    lbl_info = Label(
        master=right_output_pad_title,
        font=('arial', 10, 'bold'),
        text='输出结果统计',
        bd=2,
        anchor='w'
    )
    lbl_info.grid(row=0, column=0)

    # ============================输出信息面板=========================
    txtReceipt = Text(right_output_pad_info,
                      font=('arial', 7),
                      height=22,
                      width=62,
                      bd=9,
                      bg="white",
                      state=DISABLED)
    txtReceipt.grid(row=1, column=0)
    # ===========================Button==============================
    btn_run = Button(
        master=right_output_pad_button,
        padx=20, pady=1, fg="black",
        font=('arial', 9, 'bold'),
        width=5,
        text="启动仿真",
        command=cost_of_item
    ).grid(row=0, column=0)
    btn_analyze = Button(
        master=right_output_pad_button,
        padx=20, pady=1, fg="black",
        font=('arial', 9, 'bold'),
        width=5,
        text="仿真分析",
        command=cost_of_item
    ).grid(row=0, column=1)
    btn_exit = Button(
        master=right_output_pad_button,
        padx=20, pady=1, fg="black",
        font=('arial', 9, 'bold'),
        width=5,
        text="退出",
        command=q_exit
    ).grid(row=0, column=2)
    # ========================================================
