# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox

from src.fram_r.frame_r_view import ConfigApp

root = Tk()
# root.geometry("1350x750+0+0")
root.title('杭州分拣中心仿真程序')
root.config(
    background='#A2B5CD'
)


class App(Frame):
    """"""
    def __init__(self, master=None, pack: dict=None, attr: dict=None):
        super().__init__(master=master)
        self.pack_dic = pack
        self.attr = attr
        self._init_frame()

    def _init_frame(self):
        if self.pack_dic:
            self.pack(self.pack_dic)
        else:
            self.pack()
        if self.attr:
            self.config(self.attr)


#  顶部标题面板
Top = App(
    master=root,
    pack=ConfigApp.TOP_FRAME['pack'],
    attr=ConfigApp.TOP_FRAME['attr'])
#  左侧设置基底面板
Left = App(
    master=root, pack=ConfigApp.LEFT_FRAME['pack'],
    attr=ConfigApp.LEFT_FRAME['attr'])
#  右侧输出基底面板
Right = App(
    master=root,
    pack=ConfigApp.RIGHT_FRAME['pack'],
    attr=ConfigApp.RIGHT_FRAME['attr'])
#  右侧上部输出面板
RightOutPutPad = App(
    master=Right,
    pack=ConfigApp.RIGHT_OUTPUT_PAD['pack'],
    attr=ConfigApp.RIGHT_OUTPUT_PAD['attr'])
#  右侧下部按钮控件
RightOutPutButton = App(
    master=Right,
    pack=ConfigApp.RIGHT_OUTPUT_BUTTON['pack'],
    attr=ConfigApp.RIGHT_OUTPUT_BUTTON['attr'])
#  左侧设置面板顶部
LeftSetPadTop = App(
    master=Left,
    pack=ConfigApp.LEFT_SET_PAD_TOP['pack'],
    attr=ConfigApp.LEFT_SET_PAD_TOP['attr'])
#  左侧设置面板底部
LeftSetBottom = App(
    master=Left,
    pack=ConfigApp.LEFT_SET_PAD_BOTTOM['pack'],
    attr=ConfigApp.LEFT_SET_PAD_BOTTOM['attr'])

# LeftSetPadTopPackage = App(
#     master=LeftSetPadTop,
# )
# LeftSetPadTopMachine = App(
#     master=
# )
LeftSetPadTopPackage = App(
    master=LeftSetPadTop,
    pack=ConfigApp.LEFT_SET_PAD_TOP_PACKAGE['pack'],
    attr=ConfigApp.LEFT_SET_PAD_TOP_PACKAGE['attr']
)
LeftSetPadBottomResource = App(
    master=LeftSetBottom,
    pack=ConfigApp.LEFT_SET_PAD_BOTTOM_RESOURCE['pack'],
    attr=ConfigApp.LEFT_SET_PAD_BOTTOM_RESOURCE['attr']
)

f1aa = Frame(LeftSetPadTop, width=330, height=330, bd=8, relief='raise')
f1aa.pack(side='left')

f1ab = Frame(LeftSetPadTop, width=330, height=330, bd=8, relief='raise')
f1ab.pack(side='right')

#
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

E_R1 = StringVar()
E_R2 = StringVar()
E_R3 = StringVar()
E_R4 = StringVar()
E_R5 = StringVar()
E_R6 = StringVar()
E_R7 = StringVar()
E_R8 = StringVar()
E_R9 = StringVar()
E_R10 = StringVar()
E_R11 = StringVar()
E_R12 = StringVar()

E_R1.set('关机')
E_R2.set('关机')
E_R3.set('关机')
E_R4.set('关机')
E_R5.set('关机')
E_R6.set('关机')
E_R7.set('关机')
E_R8.set('关机')
E_R9.set('关机')
E_R10.set('关机')
E_R11.set('关机')
E_R12.set('关机')


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


#  ===============================Heading====================================
lbl_info = Label(Top, font=('arial', 20, 'bold'),
                 text='\t\t\t\t          杭州分拣中心仿真系统            \t\t\t\t',
                 bd=10, anchor='w')
lbl_info.grid(row=0, column=0)

r1 = Checkbutton(f1aa, text='r1 \t', variable=var1, onvalue=1, offvalue=0,
                 font=('arial', 18, 'bold'), command=chk_button_value).grid(
    row=0, sticky='w')

r2 = Checkbutton(f1aa, text='r2 \t\t', variable=var2, onvalue=1, offvalue=0,
                 font=('arial', 18, 'bold'), command=chk_button_value).grid(
    row=1, sticky='w')

r3 = Checkbutton(f1aa, text='r3 \t\t', variable=var3, onvalue=1, offvalue=0,
                 font=('arial', 18, 'bold'), command=chk_button_value).grid(
    row=2, sticky='w')

r4 = Checkbutton(f1aa, text='r4 \t', variable=var4, onvalue=1, offvalue=0,
                 font=('arial', 18, 'bold'), command=chk_button_value).grid(
    row=3, sticky='w')

r5 = Checkbutton(f1aa, text='r5 \t\t', variable=var5, onvalue=1, offvalue=0,
                 font=('arial', 18, 'bold'), command=chk_button_value).grid(
    row=4, sticky='w')

r6 = Checkbutton(f1aa, text='r6 \t\t', variable=var6, onvalue=1, offvalue=0,
                 font=('arial', 18, 'bold'), command=chk_button_value).grid(
    row=5, sticky='w')

txt_r1 = Entry(f1aa, font=('arial', 16, 'bold'),
               textvariable=E_R1, bd=8, width=6, justify='left', state=DISABLED)
txt_r1.grid(row=0, column=1)
txt_r2 = Entry(f1aa, font=('arial', 16, 'bold'),
               textvariable=E_R2, bd=8, width=6, justify='left', state=DISABLED)
txt_r2.grid(row=1, column=1)
txt_r3 = Entry(f1aa, font=('arial', 16, 'bold'),
               textvariable=E_R3, bd=8, width=6, justify='left', state=DISABLED)
txt_r3.grid(row=2, column=1)
txt_r4 = Entry(f1aa, font=('arial', 16, 'bold'),
               textvariable=E_R4, bd=8, width=6, justify='left', state=DISABLED)
txt_r4.grid(row=3, column=1)
txt_r5 = Entry(f1aa, font=('arial', 16, 'bold'),
               textvariable=E_R5, bd=8, width=6, justify='left', state=DISABLED)
txt_r5.grid(row=4, column=1)
txt_r6 = Entry(f1aa, font=('arial', 16, 'bold'),
               textvariable=E_R6, bd=8, width=6, justify='left', state=DISABLED)
txt_r6.grid(row=5, column=1)

r7 = Checkbutton(f1ab, text='r7 \t', variable=var7, onvalue=1, offvalue=0,
                 font=('arial', 18, 'bold'), command=chk_button_value).grid(
    row=0, sticky='w')

r8 = Checkbutton(f1ab, text='r8 \t\t', variable=var8, onvalue=1, offvalue=0,
                 font=('arial', 18, 'bold'), command=chk_button_value).grid(
    row=1, sticky='w')

r9 = Checkbutton(f1ab, text='r3 \t\t', variable=var9, onvalue=1, offvalue=0,
                 font=('arial', 18, 'bold'), command=chk_button_value).grid(
    row=2, sticky='w')

r10 = Checkbutton(f1ab, text='r4 \t', variable=var10, onvalue=1, offvalue=0,
                  font=('arial', 18, 'bold'), command=chk_button_value).grid(
    row=3, sticky='w')

r11 = Checkbutton(f1ab, text='r5 \t\t', variable=var11, onvalue=1, offvalue=0,
                  font=('arial', 18, 'bold'), command=chk_button_value).grid(
    row=4, sticky='w')

r12 = Checkbutton(f1ab, text='r6 \t\t', variable=var12, onvalue=1, offvalue=0,
                  font=('arial', 18, 'bold'), command=chk_button_value).grid(
    row=5, sticky='w')

txt_r7 = Entry(f1ab, font=('arial', 16, 'bold'),
               textvariable=E_R7, bd=8, width=6,
               justify='left', state=DISABLED)
txt_r7.grid(row=0, column=1)
txt_r8 = Entry(f1ab, font=('arial', 16, 'bold'),
               textvariable=E_R8, bd=8, width=6,
               justify='left', state=DISABLED)
txt_r8.grid(row=1, column=1)
txt_r9 = Entry(f1ab, font=('arial', 16, 'bold'),
               textvariable=E_R9, bd=8, width=6,
               justify='left', state=DISABLED)
txt_r9.grid(row=2, column=1)
txt_r10 = Entry(f1ab, font=('arial', 16, 'bold'),
                textvariable=E_R10, bd=8, width=6,
                justify='left', state=DISABLED)
txt_r10.grid(row=3, column=1)
txt_r11 = Entry(f1ab, font=('arial', 16, 'bold'),
                textvariable=E_R11, bd=8, width=6,
                justify='left', state=DISABLED)

txt_r11.grid(row=4, column=1)
txt_r12 = Entry(f1ab, font=('arial', 16, 'bold'),
                textvariable=E_R12, bd=8, width=6,
                justify='left', state=DISABLED)
txt_r12.grid(row=5, column=1)


lblReceipt = Label(RightOutPutPad, font=('arial', 12, 'bold'), text='统计面板',
                   bd=2, anchor='w')
lblReceipt.grid(row=0, column=0, sticky='w')
txtReceipt = Text(RightOutPutPad, font=('arial', 11, 'bold'), height=22, bd=8,
                  bg="white")
txtReceipt.grid(row=1, column=0)

# =====================Button==============================
btnTotal = Button(RightOutPutButton, padx=16, pady=1, bd=4, fg="black",
                  font=('arial', 16, 'bold'), width=5,
                  text="仿真", command=cost_of_item).grid(row=0, column=0)

btnExit = Button(RightOutPutButton, padx=16, pady=4, fg="black",
                 font=('arial', 16, 'bold'),
                 width=5, text="退出", command=q_exit).grid(row=0, column=1)

root.mainloop()
