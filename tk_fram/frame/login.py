import tkinter as tk
from . import create_frame
import pymysql


# 设置窗口居中
def window_info(window):
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - 200
    y = (hs / 2) - 200
    window.maxsize(483, 300)
    window.minsize(483, 300)
    return x, y


def login(window, user, passwd, message):
    conn = pymysql.connect(host='10.0.149.62', user='root', passwd='root123',
                           db='hangzhouhubqa_bian_v3')
    with conn as cur:
        cur.execute(
            "select password from authenticate where user='{}'".format(user)
        )
        result = cur.fetchone()
    if result and result[0] == passwd:
        window.destroy()
        create_frame()
    else:
        message['text'] = '账号或密码错误'


def usr_sign_up():
    pass


def creaat_login():
    # 设置登陆窗口属性
    window = tk.Tk()
    window.title('云镜·杭V1.1')
    a, b = window_info(window)
    window.geometry("450x300+%d+%d" % (a, b))
    # 登陆界面的信息
    tk.Label(window, text="仿真登陆窗口", font=("宋体", 32)).place(x=100, y=50)
    tk.Label(window, text="账号：").place(x=120, y=150)
    tk.Label(window, text="密码：").place(x=120, y=190)

    message = tk.Label(window, text="")
    message.place(x=190, y=220)
    # 显示输入框
    var_usr_name = tk.StringVar()
    # 显示默认账号
    entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
    entry_usr_name.place(x=190, y=150)
    var_usr_pwd = tk.StringVar()
    # 设置输入密码后显示*号
    entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
    entry_usr_pwd.bind('<Return>', lambda x: login(
        window, var_usr_name.get(), var_usr_pwd.get(), message
    ))
    entry_usr_pwd.place(x=190, y=190)

    btn_login = tk.Button(
        window, text="登陆", width=16,
        command=lambda: login(
            window, var_usr_name.get(), var_usr_pwd.get(), message
        ))
    btn_login.place(x=190, y=250)
    entry_usr_name.focus_set()
    # btn_sign_up = tk.Button(window,text="注册",command=usr_sign_up)
    # btn_sign_up.place(x=270,y=230)
    window.mainloop()
