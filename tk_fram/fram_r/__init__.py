#
from tkinter import messagebox
from .frame import App, CheckBtnCreate, EntryCreate
from .frame_r import init_r_frame
from .frame_r_view import *


root = Tk()

def create_r_frame():
    """"""
    #  =======================添加主视图====================
    root = Tk()
    #  =======================配置主视图尺寸=================
    root.geometry(f"{FRAME_WIDTH}x{FRAME_HEIGHT}+0+0")
    root.title('杭州分拣中心仿真程序')
    # root.minsize(FRAME_WIDTH, FRAME_HEIGHT)
    # root.maxsize(FRAME_WIDTH, FRAME_HEIGHT)
    #  =======================config主界面=================
    root.config(
        background='#A2B5CD'
    )
    #  =======================初始化r路侧界面================
    init_r_frame(root=root)
    #  =======================启动主界面====================
    root.mainloop()
