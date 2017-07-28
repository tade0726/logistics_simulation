# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
import random
import time
import datetime


root = Tk()
root.title('Cafe manager Sys')
root.config(background='black')

Top = Frame(root, width=1350, height=100, bd=14, relief='raise')
Top.pack(side='top')
#
f1 = Frame(root, width=900, height=650, bd=8, relief='raise')
f1.pack(side='left')
f2 = Frame(root, width=440, height=650, bd=8, relief='raise')
f2.pack(side='right')
#
#
ft2 = Frame(f2, width=440, height=650, bd=12, relief='raise')
ft2.pack(side='top')
fb2 = Frame(f2, width=440, height=50, bd=16, relief='raise')
fb2.pack(side='bottom')
#
f1a = Frame(f1, width=900, height=330, bd=8, relief='raise')
f1a.pack(side='top')
f2a = Frame(f1, width=900, height=320, bd=6, relief='raise')
f2a.pack(side='bottom')

f1aa = Frame(f1a, width=400, height=330, bd=16, relief='raise')
f1aa.pack(side='left')
f1ab = Frame(f1a, width=400, height=330, bd=16, relief='raise')
f1ab.pack(side='right')

f2aa = Frame(f2a, width=450, height=330, bd=14, relief='raise')
f1aa.pack(side='right')



Top.config(background='black')
f1.config(background='black')
f2.config(background='black')

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
# var13 = IntVar()
# var14 = IntVar()
# var15 = IntVar()
# var16 = IntVar()

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

def CostofItem():
    """"""
    pass


def chkbutton_value():
    """"""
    pass


def qExit():
    qExit = messagebox.askyesno("tkmessage","要退出了，确定？")
    if qExit > 0:
        root.destroy()
        return


# ===================================Heading====================================
lbl_info = Label(Top, font=('arial', 30, 'bold'), text=' 杭州分拣中心仿真系统  ',
                 bd=10, anchor='w')
lbl_info.grid(row=0, column=0)



r1 = Checkbutton(f1aa, text='r1 \t', variable=var1, onvalue=1, offvalue=0,
                    font=('arial', 18, 'bold'), command=chkbutton_value).grid(
    row=0, sticky='w')

r2 = Checkbutton(f1aa, text='r2 \t\t', variable=var2, onvalue=1, offvalue=0,
                    font=('arial', 18, 'bold'), command=chkbutton_value).grid(
    row=1, sticky='w')

r3 = Checkbutton(f1aa, text='r3 \t\t', variable=var3, onvalue=1, offvalue=0,
                    font=('arial', 18, 'bold'), command=chkbutton_value).grid(
    row=2, sticky='w')

r4 = Checkbutton(f1aa, text='r4 \t', variable=var4, onvalue=1, offvalue=0,
                    font=('arial', 18, 'bold'), command=chkbutton_value).grid(
    row=3, sticky='w')

r5 = Checkbutton(f1aa, text='r5 \t\t', variable=var5, onvalue=1, offvalue=0,
                    font=('arial', 18, 'bold'), command=chkbutton_value).grid(
    row=4, sticky='w')

r6 = Checkbutton(f1aa, text='r6 \t\t', variable=var6, onvalue=1, offvalue=0,
                    font=('arial', 18, 'bold'), command=chkbutton_value).grid(
    row=5, sticky='w')

txt_r1 = Entry(f1aa, font=('arial', 16, 'bold'),
                        textvariable=E_R1, bd=8, width=6,
                        justify='left', state=DISABLED)
txt_r1.grid(row=0, column=1)
txt_r2 = Entry(f1aa, font=('arial', 16, 'bold'),
                        textvariable=E_R2, bd=8, width=6,
                        justify='left', state=DISABLED)
txt_r2.grid(row=1, column=1)
txt_r3 = Entry(f1aa, font=('arial', 16, 'bold'),
                        textvariable=E_R3, bd=8, width=6,
                        justify='left', state=DISABLED)
txt_r3.grid(row=2, column=1)
txt_r4 = Entry(f1aa, font=('arial', 16, 'bold'),
                        textvariable=E_R4, bd=8, width=6,
                        justify='left', state=DISABLED)
txt_r4.grid(row=3, column=1)
txt_r5 = Entry(f1aa, font=('arial', 16, 'bold'),
                        textvariable=E_R5, bd=8, width=6,
                        justify='left', state=DISABLED)
txt_r5.grid(row=4, column=1)
txt_r6 = Entry(f1aa, font=('arial', 16, 'bold'),
                        textvariable=E_R6, bd=8, width=6,
                        justify='left', state=DISABLED)
txt_r6.grid(row=5, column=1)

r7 = Checkbutton(f1ab, text='r7 \t', variable=var7, onvalue=1, offvalue=0,
                    font=('arial', 18, 'bold'), command=chkbutton_value).grid(
    row=0, sticky='w')

r8 = Checkbutton(f1ab, text='r8 \t\t', variable=var8, onvalue=1, offvalue=0,
                    font=('arial', 18, 'bold'), command=chkbutton_value).grid(
    row=1, sticky='w')

r9 = Checkbutton(f1ab, text='r3 \t\t', variable=var9, onvalue=1, offvalue=0,
                    font=('arial', 18, 'bold'), command=chkbutton_value).grid(
    row=2, sticky='w')

r10 = Checkbutton(f1ab, text='r4 \t', variable=var10, onvalue=1, offvalue=0,
                    font=('arial', 18, 'bold'), command=chkbutton_value).grid(
    row=3, sticky='w')

r11 = Checkbutton(f1ab, text='r5 \t\t', variable=var11, onvalue=1, offvalue=0,
                    font=('arial', 18, 'bold'), command=chkbutton_value).grid(
    row=4, sticky='w')

r12 = Checkbutton(f1ab, text='r6 \t\t', variable=var12, onvalue=1, offvalue=0,
                    font=('arial', 18, 'bold'), command=chkbutton_value).grid(
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


lblReceipt = Label(ft2, font=('arial', 12, 'bold'), text='统计面板',
                   bd=2, anchor='w')
lblReceipt.grid(row=0, column=0, sticky='w')
txtReceipt = Text(ft2, font=('arial', 11, 'bold'), height=22, bd=8, bg="gray")
txtReceipt.grid(row=1, column=0)

# =====================Button==============================
btnTotal = Button(fb2, padx=16, pady=1, bd=4, fg="black",
                  font=('arial', 16, 'bold'), width=5,
				  text="仿真", command=CostofItem).grid(row=0, column=0)
btnExit = Button(fb2, padx=16, pady=4, fg="black", font=('arial', 16, 'bold'),
                 width=5, text="退出", command=qExit).grid(row=0, column=1)

root.mainloop()
