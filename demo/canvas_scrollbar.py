from tkinter import *
dict = {}
Liste = ["bir","iki","üç","4",5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
a = 1

####### ekleme basi ##################################################
pencere = Tk()
pencere.geometry("{0}x{1}".format(100, 100))

labelFrame = LabelFrame(pencere, width = 100, height = 100)
labelFrame.pack(side="left",fill=BOTH)
canvas = Canvas(labelFrame,relief=SUNKEN)
#canvas.config(scrollregion=(0,0,300,1000))    # halloldu =)

scrollbar = Scrollbar(labelFrame)
scrollbar.config(command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right",fill=Y)
canvas.pack(side="left",expand=YES,fill=BOTH)

frame = Frame(canvas,width=100,height=100)
frame.pack(side="top",fill=BOTH)
canvas.create_window(0,0,window=frame, anchor="nw")
####### ekleme sonu ##################################################

bas = [0, 0, 0, 100]
for i in Liste:
    dict["a%s"%a] = Checkbutton(frame, font=('Times', 18, 'bold'),onvalue=1,offvalue=0,bd=9)    # "frame" ekledim
    dict["a%s"%a].grid(row=a)
    dict["b%s" % a] = Entry(frame, font=('Times', 18, 'bold'), bd=8,width=5,justify=LEFT,state=DISABLED)  # "frame" ekledim
    dict["b%s" % a].grid(row=a, column=1)
    canvas["scrollregion"] = "%d %d %d %d" %(bas[0], bas[1], bas[2], bas[3])
    bas[3] += 16    # "scrollregion" i dinamik olarak arttir (degistirebilirsiniz)
    a += 1


mainloop()