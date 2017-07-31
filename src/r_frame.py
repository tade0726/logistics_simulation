# -*- coding: utf-8 -*-

from src.config_frame import *
from src import App, CheckBtnCreate, EntryCreate
from . import messagebox


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
    #  顶部标题面板
    top = init_app(master=root, wig='TOP_FRAME')
    #  左侧设置基底面板
    left = init_app(master=root, wig='LEFT_FRAME')
    #
    left_set_pad_package = init_app(
        master=left,
        wig='LEFT_SET_PAD_TOP_PACKAGE'
    )
    #  左侧设置面板设置
    left_set_pad_r = init_app(
        master=left,
        wig='LEFT_SET_PAD_TOP_R')
    # #  左侧设置面板底部
    left_set_pad_resource = init_app(
        master=left,
        wig='LEFT_SET_PAD_BOTTOM_RESOURCE')
    # left_set_pad_resource.grid(row=1, column=0)
    #  右侧输出基底面板
    right = init_app(
        master=root,
        wig='RIGHT_FRAME')
    right_output_pad_title = init_app(
        master=right,
        wig='RIGHT_TITLE'
    )
    #  右侧上部输出面板
    right_output_pad_info = init_app(
        master=right,
        wig='RIGHT_OUTPUT_PAD_INFO')
    #  右侧下部按钮控件
    right_output_pad_button = init_app(
        master=right,
        wig='RIGHT_BUTTON')
    # LeftSetPadTopMachine = App(
    #     master=
    # )

    # left_set_pad_bottom_resource = init_app(
    #     master=left_set_bottom,
    #     wig='LEFT_SET_PAD_BOTTOM_RESOURCE'
    # )
    left_set_pad_center_left = init_app(
        master=left_set_pad_r,
        wig='LEFT_SET_PAD_CENTER_LEFT'
    )
    left_set_pad_center_right = init_app(
        master=left_set_pad_r,
        wig='LEFT_SET_PAD_CENTER_RIGHT'
    )
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

    e_r1.set('关机')
    e_r2.set('关机')
    e_r3.set('关机')
    e_r4.set('关机')
    e_r5.set('关机')
    e_r6.set('关机')
    e_r7.set('关机')
    e_r8.set('关机')
    e_r9.set('关机')
    e_r10.set('关机')
    e_r11.set('关机')
    e_r12.set('关机')
    e_r13.set('关机')
    e_r14.set('关机')
    e_r15.set('关机')
    e_r16.set('关机')
    e_r17.set('关机')
    e_r18.set('关机')
    e_r19.set('关机')
    e_r20.set('关机')
    e_r21.set('关机')
    e_r22.set('关机')
    e_r23.set('关机')
    e_r24.set('关机')
    e_r25.set('关机')
    e_r26.set('关机')
    e_r27.set('关机')
    e_r28.set('关机')
    e_r29.set('关机')
    e_r30.set('关机')
    e_r31.set('关机')
    e_r32.set('关机')

    def cost_of_item():
        """"""
        pass

    def chk_button_value():
        """"""
        pass

    def q_exit():
        if_exit = messagebox.askyesno("tkmessage", "要退出了，确定？")
        if if_exit > 0:
            root.destroy()
            return

    # ==============================Heading===========================
    lbl_info = Label(top,
                     font=('arial', 20, 'bold'),
                     text='\t\t\t\t杭州分拣中心仿真系统\t\t\t\t',
                     bd=10,
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
        width=70
    )
    package_num.grid(row=0, column=1)
    # ============================机器配置==========================
    # # 路侧卸货标题
    # lbl_unload = Label(
    #     master=left_set_pad_center_left,
    #     font=('arial', 10),
    #     text='路侧设置面板',
    #     bd=2,
    #     anchor='w'
    # )
    # lbl_unload.grid(row=0, column=0)
    # =============================================================
    r1_1 = init_check_btn(
        master=left_set_pad_center_left, id='r1_1', var=var1,
        command=chk_button_value)
    txt_r1_1 = init_entry(
        master=left_set_pad_center_left, id='r1_1', text_var=e_r1)
    r1_2 = init_check_btn(
        master=left_set_pad_center_left, id='r1_2', var=var2,
        command=chk_button_value)
    txt_r1_2 = init_entry(
        master=left_set_pad_center_left, id='r1_2', text_var=e_r2)
    r1_3 = init_check_btn(
        master=left_set_pad_center_left, id='r1_3', var=var3,
        command=chk_button_value)
    txt_r1_3 = init_entry(
        master=left_set_pad_center_left, id = 'r1_3', text_var=e_r3)
    r1_4 = init_check_btn(
        master=left_set_pad_center_left, id='r1_4', var=var4,
        command=chk_button_value)
    txt_r1_4 = init_entry(
        master=left_set_pad_center_left, id='r1_4', text_var=e_r4)
    # ==================================================================
    r2_1 = init_check_btn(
        master=left_set_pad_center_left, id='r2_1', var=var5,
        command=chk_button_value)
    txt_r2_1 = init_entry(
        master=left_set_pad_center_left, id='r2_1', text_var=e_r5)
    r2_2 = init_check_btn(
        master=left_set_pad_center_left, id='r2_2', var=var6,
        command=chk_button_value)
    txt_r2_2 = init_entry(
        master=left_set_pad_center_left, id='r2_2', text_var=e_r6)
    r2_3 = init_check_btn(
        master=left_set_pad_center_left, id='r2_3', var=var7,
        command=chk_button_value)
    txt_r2_3 = init_entry(
        master=left_set_pad_center_left, id='r2_3', text_var=e_r7)
    r2_4 = init_check_btn(
        master=left_set_pad_center_left, id='r2_4', var=var8,
        command=chk_button_value)
    txt_r2_4 = init_entry(
        master=left_set_pad_center_left, id='r2_4', text_var=e_r8)
    # =======================================================================
    r3_1 = init_check_btn(
        master=left_set_pad_center_left, id='r3_1', var=var9,
        command=chk_button_value)
    txt_r3_1 = init_entry(
        master=left_set_pad_center_left, id='r3_1', text_var=e_r9)
    r3_2 = init_check_btn(
        master=left_set_pad_center_left, id='r3_2', var=var10,
        command=chk_button_value)
    txt_r3_2 = init_entry(
        master=left_set_pad_center_left, id='r3_2', text_var=e_r10)
    r3_3 = init_check_btn(
        master=left_set_pad_center_left, id='r3_3', var=var11,
        command=chk_button_value)
    txt_r3_3 = init_entry(
        master=left_set_pad_center_left, id='r3_3', text_var=e_r11)
    r3_4 = init_check_btn(
        master=left_set_pad_center_left, id='r3_4', var=var12,
        command=chk_button_value)
    txt_r3_4 = init_entry(
        master=left_set_pad_center_left, id='r3_4', text_var=e_r12)
    # =======================================================================
    r4_1 = init_check_btn(
        master=left_set_pad_center_left, id='r4_1', var=var13,
        command=chk_button_value)
    txt_r4_1 = init_entry(
        master=left_set_pad_center_left, id='r4_1', text_var=e_r13)
    r4_2 = init_check_btn(
        master=left_set_pad_center_left, id='r4_2', var=var14,
        command=chk_button_value)
    txt_r4_2 = init_entry(
        master=left_set_pad_center_left, id='r4_2', text_var=e_r14)
    r4_3 = init_check_btn(
        master=left_set_pad_center_left, id='r4_3', var=var15,
        command=chk_button_value)
    txt_r4_3 = init_entry(
        master=left_set_pad_center_left, id='r4_3', text_var=e_r15)
    r4_4 = init_check_btn(
        master=left_set_pad_center_left, id='r4_4', var=var16,
        command=chk_button_value)
    txt_r4_4 = init_entry(
        master=left_set_pad_center_left, id='r4_4', text_var=e_r16)
    # =================================2=============================
    r5_1 = init_check_btn(
        master=left_set_pad_center_left, id='r5_1', var=var17,
        command=chk_button_value)
    txt_r5_1 = init_entry(
        master=left_set_pad_center_left, id='r5_1', text_var=e_r17)
    r5_2 = init_check_btn(
        master=left_set_pad_center_left, id='r5_2', var=var18,
        command=chk_button_value)
    txt_r5_2 = init_entry(
        master=left_set_pad_center_left, id='r5_2', text_var=e_r18)
    r5_3 = init_check_btn(
        master=left_set_pad_center_left, id='r5_3', var=var19,
        command=chk_button_value)
    txt_r5_3 = init_entry(
        master=left_set_pad_center_left, id='r5_3', text_var=e_r19)
    r5_4 = init_check_btn(
        master=left_set_pad_center_left, id='r5_4', var=var20,
        command=chk_button_value)
    txt_r5_4 = init_entry(
        master=left_set_pad_center_left, id='r5_4', text_var=e_r20)
    # # ===========================空侧卸货口设置==============================
    # a1_1 = init_check_btn(
    #     master=left_set_pad_center_right, id='a1_1', var=var21,
    #     command=chk_button_value)
    # txt_a1_1 = init_entry(
    #     master=left_set_pad_center_right, id='a1_1', text_var=e_r21)
    # a1_2 = init_check_btn(
    #     master=left_set_pad_center_right, id='a1_2', var=var22,
    #     command=chk_button_value)
    # txt_a1_2 = init_entry(
    #     master=left_set_pad_center_right, id='a1_2', text_var=e_r22)
    # a1_3 = init_check_btn(
    #     master=left_set_pad_center_right, id='a1_3', var=var23,
    #     command=chk_button_value)
    # txt_a1_3 = init_entry(
    #     master=left_set_pad_center_right, id='a1_3', text_var=e_r23)
    # a1_4 = init_check_btn(
    #     master=left_set_pad_center_right, id='a1_4', var=var24,
    #     command=chk_button_value)
    # txt_a1_4 = init_entry(
    #     master=left_set_pad_center_right, id='a1_4', text_var=e_r24)
    # # =======================================================================
    # a1_5 = init_check_btn(
    #     master=left_set_pad_center_right, id='a1_5', var=var25,
    #     command=chk_button_value)
    # txt_a1_5 = init_entry(
    #     master=left_set_pad_center_right, id='a1_5', text_var=e_r25)
    # a1_6 = init_check_btn(
    #     master=left_set_pad_center_right, id='a1_6', var=var26,
    #     command=chk_button_value)
    # txt_a1_6 = init_entry(
    #     master=left_set_pad_center_right, id='a1_6', text_var=e_r26)
    # a1_7 = init_check_btn(
    #     master=left_set_pad_center_right, id='a1_7', var=var27,
    #     command=chk_button_value)
    # txt_a1_7 = init_entry(
    #     master=left_set_pad_center_right, id='a1_7', text_var=e_r27)
    # a1_8 = init_check_btn(
    #     master=left_set_pad_center_right, id='a1_8', var=var28,
    #     command=chk_button_value)
    # txt_a1_8 = init_entry(
    #     master=left_set_pad_center_right, id='a1_8', text_var=e_r28)
    # # =======================================================================
    # a1_9 = init_check_btn(
    #     master=left_set_pad_center_right, id='a1_9', var=var29,
    #     command=chk_button_value)
    # txt_a1_9 = init_entry(
    #     master=left_set_pad_center_right, id='a1_9', text_var=e_r29)
    # a1_10 = init_check_btn(
    #     master=left_set_pad_center_right, id='a1_10', var=var30,
    #     command=chk_button_value)
    # txt_a1_10 = init_entry(
    #     master=left_set_pad_center_right, id='a1_10', text_var=e_r30)
    # a1_11 = init_check_btn(
    #     master=left_set_pad_center_right, id='a1_11', var=var31,
    #     command=chk_button_value)
    # txt_a1_11 = init_entry(
    #     master=left_set_pad_center_right, id='a1_11', text_var=e_r31)
    # a1_12 = init_check_btn(
    #     master=left_set_pad_center_right, id='a1_12', var=var32,
    #     command=chk_button_value)
    # txt_a1_12 = init_entry(
    #     master=left_set_pad_center_right, id='a1_12', text_var=e_r32)
    # ============================资源配置=============================
    # 标题
    lbl_resource = Label(
        master=left_set_pad_resource,
        font=('arial', 12),
        text='人力资源数：',
        bd=2,
        anchor='w'
    )
    lbl_resource.grid(row=0, column=0)
    # 选择人数
    person_res = Spinbox(
        master=left_set_pad_resource,
        values=(1, 2))
    person_res.grid(row=0, column=1)
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
                      font=('arial', 11, 'bold'),
                      height=23,
                      bd=8,
                      bg="white")
    txtReceipt.grid(row=0, column=0)
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
