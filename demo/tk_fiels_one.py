from tkinter import *
from tkinter.messagebox  import *
from tkinter import Menu
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Separator

root=Tk()


def callback():
    askopenfilename()


errmsg = '确认导入文件？'
Button(master=root,text='选择文件', command=callback).pack(fill=X)
sepa = Separator(master=root, orient='horizontal')
Button(master=root, text='导入',
       command=(lambda: showerror('Spam', errmsg))).pack(fill=X)
mainloop()
