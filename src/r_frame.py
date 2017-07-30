# -*- coding: utf-8 -*-

from src.config_frame import *
from src import App
from . import messagebox


def init_app(master, wig):
    """"""

    return App(master=master,
               pack=ConfigApp.RELOAD_FRAME[wig]['pack'],
               attr=ConfigApp.RELOAD_FRAME[wig]['attr'])


def init_r_frame(root: Tk):
    """"""
    #  顶部标题面板
    top = init_app(master=root, wig='TOP_FRAME')
    #  左侧设置基底面板
    left = init_app(master=root, wig='LEFT_FRAME')
    #  右侧输出基底面板
    right = init_app(master=root, wig='RIGHT_FRAME')
    #  右侧上部输出面板
    right_output_pad = init_app(master=right, wig='RIGHT_OUTPUT_PAD')
    #  右侧下部按钮控件
    right_output_button = init_app(master=right, wig='RIGHT_OUTPUT_BUTTON')
    #  左侧设置面板顶部
    left_set_pad_top = init_app(master=left, wig='LEFT_SET_PAD_TOP')
    #  左侧设置面板底部
    left_set_bottom = init_app(master=left, wig='LEFT_SET_PAD_BOTTOM')

    # LeftSetPadTopMachine = App(
    #     master=
    # )
    left_set_pad_top_package = init_app(
        master=left_set_pad_top,
        wig='LEFT_SET_PAD_TOP_PACKAGE'
    )
    left_set_pad_bottom_resource = init_app(
        master=left_set_bottom,
        wig='LEFT_SET_PAD_BOTTOM_RESOURCE'
    )
    left_set_pad_center_left = init_app(
        master=left_set_pad_top,
        wig='LEFT_SET_PAD_CENTER_LEFT'
    )
    left_set_pad_center_right = init_app(
        master=left_set_pad_top,
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

    # ===============================Heading====================================
    lbl_info = Label(top, font=('arial', 20, 'bold'),
                     text='\t\t\t\t          杭州分拣中心仿真系统            \t\t\t\t',
                     bd=10, anchor='w')
    lbl_info.grid(row=0, column=0)

    r1 = Checkbutton(left_set_pad_center_left, text='r1 \t', variable=var1, onvalue=1, offvalue=0,
                     font=('arial', 18, 'bold'), command=chk_button_value).grid(
        row=0, sticky='w')

    r2 = Checkbutton(left_set_pad_center_left, text='r2 \t\t', variable=var2, onvalue=1, offvalue=0,
                     font=('arial', 18, 'bold'), command=chk_button_value).grid(
        row=1, sticky='w')

    r3 = Checkbutton(left_set_pad_center_left, text='r3 \t\t', variable=var3, onvalue=1, offvalue=0,
                     font=('arial', 18, 'bold'), command=chk_button_value).grid(
        row=2, sticky='w')

    r4 = Checkbutton(left_set_pad_center_left, text='r4 \t', variable=var4, onvalue=1, offvalue=0,
                     font=('arial', 18, 'bold'), command=chk_button_value).grid(
        row=3, sticky='w')

    r5 = Checkbutton(left_set_pad_center_left, text='r5 \t\t', variable=var5, onvalue=1, offvalue=0,
                     font=('arial', 18, 'bold'), command=chk_button_value).grid(
        row=4, sticky='w')

    r6 = Checkbutton(left_set_pad_center_left, text='r6 \t\t', variable=var6, onvalue=1, offvalue=0,
                     font=('arial', 18, 'bold'), command=chk_button_value).grid(
        row=5, sticky='w')

    txt_r1 = Entry(left_set_pad_center_left, font=('arial', 16, 'bold'),
                   textvariable=e_r1, bd=8, width=6, justify='left',
                   state=DISABLED)
    txt_r1.grid(row=0, column=1)
    txt_r2 = Entry(left_set_pad_center_left, font=('arial', 16, 'bold'),
                   textvariable=e_r2, bd=8, width=6, justify='left',
                   state=DISABLED)
    txt_r2.grid(row=1, column=1)
    txt_r3 = Entry(left_set_pad_center_left, font=('arial', 16, 'bold'),
                   textvariable=e_r3, bd=8, width=6, justify='left',
                   state=DISABLED)
    txt_r3.grid(row=2, column=1)
    txt_r4 = Entry(left_set_pad_center_left, font=('arial', 16, 'bold'),
                   textvariable=e_r4, bd=8, width=6, justify='left',
                   state=DISABLED)
    txt_r4.grid(row=3, column=1)
    txt_r5 = Entry(left_set_pad_center_left, font=('arial', 16, 'bold'),
                   textvariable=e_r5, bd=8, width=6, justify='left',
                   state=DISABLED)
    txt_r5.grid(row=4, column=1)
    txt_r6 = Entry(left_set_pad_center_left, font=('arial', 16, 'bold'),
                   textvariable=e_r6, bd=8, width=6, justify='left',
                   state=DISABLED)
    txt_r6.grid(row=5, column=1)

    r7 = Checkbutton(left_set_pad_center_right,
                     text='r7 \t', variable=var7, onvalue=1, offvalue=0,
                     font=('arial', 18, 'bold'), command=chk_button_value
                     ).grid(
        row=0, sticky='w')

    r8 = Checkbutton(left_set_pad_center_right, text='r8 \t\t', variable=var8, onvalue=1, offvalue=0,
                     font=('arial', 18, 'bold'), command=chk_button_value).grid(
        row=1, sticky='w')

    r9 = Checkbutton(left_set_pad_center_right, text='r3 \t\t', variable=var9, onvalue=1, offvalue=0,
                     font=('arial', 18, 'bold'), command=chk_button_value).grid(
        row=2, sticky='w')

    r10 = Checkbutton(left_set_pad_center_right, text='r4 \t', variable=var10, onvalue=1, offvalue=0,
                      font=('arial', 18, 'bold'),
                      command=chk_button_value).grid(
        row=3, sticky='w')

    r11 = Checkbutton(left_set_pad_center_right, text='r5 \t\t', variable=var11, onvalue=1,
                      offvalue=0,
                      font=('arial', 18, 'bold'),
                      command=chk_button_value).grid(
        row=4, sticky='w')

    r12 = Checkbutton(left_set_pad_center_right, text='r6 \t\t', variable=var12, onvalue=1,
                      offvalue=0,
                      font=('arial', 18, 'bold'),
                      command=chk_button_value).grid(
        row=5, sticky='w')

    txt_r7 = Entry(left_set_pad_center_right, font=('arial', 16, 'bold'),
                   textvariable=e_r7, bd=8, width=6,
                   justify='left', state=DISABLED)
    txt_r7.grid(row=0, column=1)
    txt_r8 = Entry(left_set_pad_center_right, font=('arial', 16, 'bold'),
                   textvariable=e_r8, bd=8, width=6,
                   justify='left', state=DISABLED)
    txt_r8.grid(row=1, column=1)
    txt_r9 = Entry(left_set_pad_center_right, font=('arial', 16, 'bold'),
                   textvariable=e_r9, bd=8, width=6,
                   justify='left', state=DISABLED)
    txt_r9.grid(row=2, column=1)
    txt_r10 = Entry(left_set_pad_center_right, font=('arial', 16, 'bold'),
                    textvariable=e_r10, bd=8, width=6,
                    justify='left', state=DISABLED)
    txt_r10.grid(row=3, column=1)
    txt_r11 = Entry(left_set_pad_center_right, font=('arial', 16, 'bold'),
                    textvariable=e_r11, bd=8, width=6,
                    justify='left', state=DISABLED)

    txt_r11.grid(row=4, column=1)
    txt_r12 = Entry(left_set_pad_center_right, font=('arial', 16, 'bold'),
                    textvariable=e_r12, bd=8, width=6,
                    justify='left', state=DISABLED)
    txt_r12.grid(row=5, column=1)

    lblReceipt = Label(
        right_output_pad,
        font=('arial', 12, 'bold'), text='统计面板',
        bd=2, anchor='w')
    lblReceipt.grid(row=0, column=0, sticky='w')
    txtReceipt = Text(right_output_pad, font=('arial', 11, 'bold'), height=22,
                      bd=8,
                      bg="white")
    txtReceipt.grid(row=1, column=0)

    # =====================Button==============================
    btnTotal = Button(right_output_button, padx=16, pady=1, bd=4, fg="black",
                      font=('arial', 16, 'bold'), width=5,
                      text="仿真", command=cost_of_item).grid(row=0, column=0)

    btnExit = Button(right_output_button, padx=16, pady=4, fg="black",
                     font=('arial', 16, 'bold'),
                     width=5, text="退出", command=q_exit).grid(row=0, column=1)
