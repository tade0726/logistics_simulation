#
from tkinter import messagebox
from .config_frame import *
from .frame import App
from .r_frame import init_r_frame

root = Tk()

def create_r_frame():
    """"""
    # root.geometry("1350x750+0+0")
    root.title('杭州分拣中心仿真程序')
    root.config(
        background='#A2B5CD'
    )
    init_r_frame(root=root)
    root.mainloop()
