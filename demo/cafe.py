from tkinter import *
from tkinter import messagebox

root = Tk()
root.geometry("1350x750+0+0")
root.title("机场数据分析系统")
root.configure(background='black')

Tops = Frame(root, width=1350, height=100, bd=14, relief='raise')
Tops.pack(side=TOP)

f1 = Frame(root, width=900, height=650, bd=8, relief='raise')
f1.pack(side=LEFT)
f2 = Frame(root, width=440, height=650, bd=8, relief='raise')
f2.pack(side=RIGHT)

ft2 = Frame(f2, width=440, height=650, bd=12, relief='raise')
ft2.pack(side=TOP)
fb2 = Frame(f2, width=440, height=50, bd=16, relief='raise')
fb2.pack(side=BOTTOM)

f1a = Frame(f1, width=900, height=330, bd=8, relief='raise')
f1a.pack(side=TOP)
f2a = Frame(f1, width=900, height=320, bd=6, relief='raise')
f2a.pack(side=BOTTOM)

f1aa = Frame(f1a, width=400, height=330, bd=16, relief='raise')
f1aa.pack(side=LEFT)
f1ab = Frame(f1a, width=400, height=330, bd=16, relief='raise')
f1ab.pack(side=RIGHT)

f2aa = Frame(f2a, width=450, height=330, bd=14, relief='raise')
f2aa.pack(side=LEFT)
f2ab = Frame(f2a, width=450, height=330, bd=14, relief='raise')
f2ab.pack(side=RIGHT)

Tops.configure(background='black')
f1.configure(background='black')
f2.configure(background='black')


# -------------------------Cost of Item-------------------------------------------------
def CostofItem():
	Item1 = float(E_Latta.get())
	Item2 = float(E_Coffee_Cake.get())

	CostofDrinks.set(Item1)
	CostofCakes.set(Item2)
	ServiceCharge.set(Item1+Item2)



	# SC = "$", str('%.2f' % 1.59)
	# ServiceCharge.set(SC)
	#
	# SubTotalofITEMS = '$', str('%.2f' % (PriceofDrinks + 1.59))
	# SubTotal.set(SubTotalofITEMS)
	#
	# Tax = '$', str('%.2f' % ((PriceofDrinks + 1.59) * 0.15))
	# PaidTax.set(Tax)
	# TT = (PriceofDrinks + 1.59) * 0.15
	# TC = '$', str('%.2f' % (PriceofDrinks + 1.59 + TT))
	# TotalCost.set(TC)


# ----------------------------Heading----------------------------------------------
lblInfo = Label(Tops, font=('arial', 70, 'bold'), text="机场数据分析系统", bd=10, anchor='w')
lblInfo.grid(row=0, column=0)


# ---------------------------Calculator----------------------------------------------
def chkbutton_value():
	if var1.get() == 1:
		txtLatta.configure(state=NORMAL)
	elif var1.get() == 0:
		txtLatta.configure(state=DISABLED)
		E_Latta.set("0")
	if var9.get() == 1:
		txtCoffee_Cake.configure(state=NORMAL)
	elif var9.get() == 0:
		txtCoffee_Cake.configure(state=DISABLED)
		E_Coffee_Cake.set("0")

def qExit():
	qExit = messagebox.askyesno("tkmessage","要退出了，确定？")
	if qExit > 0:
		root.destroy()
		return
# -------------------------------------------------------------------------
var1 = IntVar()
# var2 = IntVar()
# var3 = IntVar()
# var4 = IntVar()
# var5 = IntVar()
# var6 = IntVar()
# var7 = IntVar()
# var8 = IntVar()
var9 = IntVar()
# var10 = IntVar()
# var11 = IntVar()
# var12 = IntVar()
# var13 = IntVar()
# var14 = IntVar()
# var15 = IntVar()
# var16 = IntVar()

CostofDrinks = StringVar()
CostofCakes = StringVar()
ServiceCharge = StringVar()
SubTotal = StringVar()
PaidTax = StringVar()
TotalCost = StringVar()
E_Coffee_Cake = StringVar()
E_Latta = StringVar()
# --------------------------------------------------------
E_Latta.set("0")
E_Coffee_Cake.set("0")

# ================================Drinks=================================
Latta = Checkbutton(f1aa, text="大物件 \t", variable=var1, onvalue=1, offvalue=0,
					font=('arial', 18, 'bold'), command=chkbutton_value).grid(row=0, sticky=W)

# ================================Cakes==================================
CoffeeCake = Checkbutton(f1ab, text="小物件 \t", variable=var9, onvalue=1, offvalue=0,
					font=('arial', 18, 'bold'), command=chkbutton_value).grid(row=0, sticky=W)

# =====================Enter Widget for Drinks===========================
txtCoffee_Cake = Entry(f1ab, font=('arial', 16, 'bold'), textvariable=E_Coffee_Cake, bd=8,
				 width=6, justify='left', state=DISABLED)
txtCoffee_Cake.grid(row=0, column=1)

# ============================Enter Widget for Cakes===========================
txtLatta = Entry(f1aa, font=('arial', 16, 'bold'), textvariable=E_Latta, bd=8,
				 width=6, justify='left', state=DISABLED)
txtLatta.grid(row=0, column=1)

# =====================Cost Items Information============================
lblCostofDrinks = Label(f2aa, font=('arial', 16, 'bold'), text='大物件数量', bd=8, anchor='w')
lblCostofDrinks.grid(row=2, column=0, sticky=W)
txtCostofDrinks = Entry(f2aa, font=('arial', 16, 'bold'), textvariable=CostofDrinks, bd=8, insertwidth=2, justify='left')
txtCostofDrinks.grid(row=2, column=1)

lblCostofCakes = Label(f2aa, font=('arial', 16, 'bold'), text='小物件数量', bd=8, anchor='w')
lblCostofCakes.grid(row=3, column=0, sticky=W)
txtCostofCakes = Entry(f2aa, font=('arial', 16, 'bold'), textvariable=CostofCakes, bd=8, insertwidth=2, justify='left')
txtCostofCakes.grid(row=3, column=1)

lblServiceCharge = Label(f2aa, font=('arial', 16, 'bold'), text='总数', bd=8, anchor='w')
lblServiceCharge.grid(row=4, column=0, sticky=W)
txtServiceCharge = Entry(f2aa, font=('arial', 16, 'bold'), textvariable=ServiceCharge, bd=8, insertwidth=2, justify='left')
txtServiceCharge.grid(row=4, column=1)


# ============================Information======================
lblReceipt = Label(ft2, font=('arial', 12, 'bold'), text='统计板', bd=2, anchor='w')
lblReceipt.grid(row=0, column=0, sticky=W)
txtReceipt = Text(ft2, font=('arial', 11, 'bold'), height=22, bd=8, bg="brown")
txtReceipt.grid(row=1, column=0)

# =====================Button==============================
btnTotal = Button(fb2, padx=16, pady=1, bd=4, fg="black", font=('arial', 16, 'bold'), width=5,
				  text="Total", command=CostofItem).grid(row=0, column=0)
btnExit = Button(fb2, padx=16, pady=4, fg="black", font=('arial', 16, 'bold'), width=5, text="Exit",
				 command=qExit).grid(row=0, column=3)
root.mainloop()
