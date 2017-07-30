#coding=utf-8
import tempfile
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from tkinter.ttk import *

import os
import shutil
from collections import OrderedDict
from ast import literal_eval
import re

import subprocess

tk=Tk()
tk.title('Renamer')
tk.rowconfigure(0,weight=1)
tk.columnconfigure(0,weight=1)

filesvar=StringVar()

book=Notebook(tk)
book.grid(row=0,column=0,sticky='nswe')

fi=Frame(book)
fe=Frame(book)
fr=Frame(book)
book.add(fi,text=' 1. 导入 ')
book.add(fe,text=' 2. 编辑 ')
book.add(fr,text=' 3. 重构 ')

##### import

fi.rowconfigure(1,weight=1)
fi.columnconfigure(3,weight=1)

def _gtfiles():
    return literal_eval(filesvar.get() or '()')

def _addfiles(files):
    old=_gtfiles()
    new=OrderedDict.fromkeys(old+tuple((os.path.normpath(x) for x in files)))
    filesvar.set(tuple(new))

def import_single(*_):
    fns=filedialog.askopenfilenames(title='导入文件……')
    _addfiles(fns)

def import_list(*_):
    tl=Toplevel(tk)
    tl.title('导入文件列表')
    tl.rowconfigure(0,weight=1)
    tl.columnconfigure(0,weight=1)

    def _do_import(*_):
        _addfiles([x.strip() for x in t.get(1.0,END).split('\n') if x.strip()])
        tl.destroy()

    t=Text(tl,font='Consolas -12')
    t.grid(row=0,column=0,sticky='nswe')
    t_sbar=Scrollbar(tl,orient=VERTICAL,command=t.yview)
    t_sbar.grid(row=0,column=1,sticky='ns')
    t['yscrollcommand'] = t_sbar.set

    Button(tl,text='批量导入',command=_do_import).grid(row=1,column=0,columnspan=2,sticky='we')

    tl.focus_force()

def import_folder(*_):
    folder=filedialog.askdirectory(title='导入目录……')
    res=[]
    warned=False
    for root,_,files in os.walk(folder,followlinks=True):
        res+=[os.path.join(root,x) for x in files]
        if not warned and len(res)>10000:
            if messagebox.askokcancel('Renamer','警告：您将要同时添加超过一万个文件'):
                warned=True
            else:
                return
    _addfiles(res)

def file_filter(*_):
    tl=Toplevel(tk)
    tl.title('过滤文件')
    tl.resizable(True,False)
    tl.columnconfigure(0,weight=1)

    mode=StringVar(value='text')
    pattern=StringVar()

    def _proc(*_):
        md=mode.get()
        if md=='text':
            return lambda x: pattern.get() in x
        elif md=='regex':
            re_exp=re.compile(pattern.get())
            return lambda x: re_exp.search(x)
        elif md=='lambda':
            return eval(pattern.get())
        else:
            raise RuntimeError('bad mode arg')

    def _preview(*_):
        res=[]
        tester=_proc()
        for fn in _gtfiles():
            if tester(fn):
                res.append(fn)
                if len(res)>20:
                    res.append('< 达到20项匹配，其余结果已截断 >')
                    break
        messagebox.showinfo(
            'Renamer',
            '匹配结果：\n\n%s\n\n这些项将被【%s】'%(('\n'.join(res)),'删除' if chb.instate(['selected']) else '保留')
        )
        tl.focus_force()

    def _do_filter(*_):
        tester=_proc()
        fns=(x for x in _gtfiles() if (not tester(x) if chb.instate(['selected']) else tester(x)))
        filesvar.set(tuple(fns))

    btn_f=Frame(tl)
    btn_f.grid(row=0,column=0,columnspan=3,sticky='we')
    Radiobutton(btn_f,text='字符串匹配',variable=mode,value='text').grid(row=0,column=0)
    Radiobutton(btn_f,text='正则表达式',variable=mode,value='regex').grid(row=0,column=1)
    Radiobutton(btn_f,text='lambda 表达式',variable=mode,value='lambda').grid(row=0,column=2)
    chb=Checkbutton(btn_f,text='删除匹配项')
    chb.grid(row=0,column=3)
    chb.state(['!alternate','!selected'])

    Entry(tl,textvariable=pattern).grid(row=1,column=0,sticky='we')
    Button(tl,text='预览',command=_preview).grid(row=1,column=1)
    Button(tl,text='过滤',command=_do_filter).grid(row=1,column=2)

    tl.focus_force()

def delete_single(*_):
    ind=lbox.curselection()
    if len(ind)==1:
        fns=list(_gtfiles())
        del fns[ind[0]]
        filesvar.set(tuple(fns))

def clear_list(*_):
    filesvar.set(())

Button(fi,text='导入文件',command=import_single).grid(row=0,column=0)
Button(fi,text='导入文件列表',command=import_list).grid(row=0,column=1)
Button(fi,text='导入目录',command=import_folder).grid(row=0,column=2)
Button(fi,text='过滤',command=file_filter).grid(row=0,column=4)
Button(fi,text='清空列表',command=clear_list).grid(row=0,column=5)

lbox_f=Frame(fi)
lbox_f.grid(row=1,column=0,columnspan=6,sticky='nswe')
lbox_f.rowconfigure(0,weight=1)
lbox_f.columnconfigure(0,weight=1)

lbox=Listbox(lbox_f,listvariable=filesvar)
lbox.grid(row=0,column=0,sticky='nswe')
lbox.bind('<Double-Button-1>',delete_single)
lbox_sbar=Scrollbar(lbox_f,orient=VERTICAL,command=lbox.yview)
lbox_sbar.grid(row=0,column=1,sticky='ns')
lbox['yscrollcommand'] = lbox_sbar.set

##### edit

fe.rowconfigure(1,weight=1)
fe.columnconfigure(1,weight=1)

def _gtcontent():
    return filter(None,fntxt.get(1.0,END).split('\n'))

def init_fn(*_):
    fntxt.delete(1.0,END)
    fntxt.insert(END,'\n'.join([os.path.split(x)[1] for x in _gtfiles()]))

def fn_replace(*_):
    tl=Toplevel(tk)
    tl.title('文件名替换')
    tl.resizable(True,False)
    tl.columnconfigure(0,weight=1)

    pattern=StringVar()
    replacer=StringVar()

    def _proc():
        if chb.instate(['selected']):
            re_exp=re.compile(pattern.get())
            return lambda x: re_exp.sub(replacer.get(),x)
        else:
            return lambda x: x.replace(pattern.get(),replacer.get())

    def preview(*_):
        procer=_proc()
        res=[]
        for fn in _gtcontent():
            res.append('%s → %s'%(fn,procer(fn)))
            if len(res)>20:
                res.append('< 超过20项结果，其余结果已截断 >')
                break
        messagebox.showinfo('Renamer','替换结果预览：\n\n%s'%('\n'.join(res)))
        tl.focus_force()

    def replace(*_):
        procer=_proc()
        fns=[procer(x) for x in _gtcontent()]
        fntxt.delete(1.0,END)
        fntxt.insert(END,'\n'.join(fns))
        tl.destroy()

    Entry(tl,textvariable=pattern).grid(row=0,column=0,columnspan=3,sticky='we')
    Entry(tl,textvariable=replacer).grid(row=1,column=0,columnspan=3,sticky='we')
    chb=Checkbutton(tl,text='正则表达式')
    chb.grid(row=2,column=0)
    chb.state(['!alternate','selected'])
    Button(tl,text='预览',command=preview).grid(row=2,column=1)
    Button(tl,text='替换',command=replace).grid(row=2,column=2)

    tl.focus_force()

def python_replace(*_):
    exp=simpledialog.askstring('输入 lambda 表达式','lambda f :')
    if exp:
        procer=eval('lambda f : '+exp)
        fns=[procer(x) for x in _gtcontent()]
        fntxt.delete(1.0,END)
        fntxt.insert(END,'\n'.join((str(x) for x in fns)))

def open_in_npp(*_):
    editors=[
        '%programfiles%/notepad++/notepad++.exe',
        '%programfiles(x86)%/notepad++/notepad++.exe',
        '%ProgramW6432%/notepad++/notepad++.exe',
        '%systemroot%/system32/notepad.exe',
        #todo: add more
    ]
    for editor in editors:
        if os.path.isfile(os.path.expandvars(editor)):
            tmpfn=tempfile.mktemp('.filenames.txt')
            old_content='\n'.join(_gtcontent())
            with open(tmpfn,'w') as f:
                f.write(old_content)
            subprocess.Popen(
                executable=os.path.expandvars('%systemroot%/system32/cmd.exe'),
                args='/c start /wait "" "%s" "%s"'%(os.path.expandvars(editor),tmpfn)
            ).wait()
            if os.path.isfile(tmpfn):
                with open(tmpfn,'r') as f:
                    new_content=f.read()
                os.remove(tmpfn)
                if old_content!=new_content and messagebox.askyesno('Renamer','是否应用外部编辑器的更改？'):
                    fntxt.delete(1.0,END)
                    fntxt.insert(END,new_content)
            break
    else:
        messagebox.showerror('Renamer','没有可用的外部编辑器')

def replace_with_ind(*_):
    tl=Toplevel(tk)
    tl.title('插入序号')
    tl.resizable(True,False)
    tl.columnconfigure(2,weight=1)

    pattern=StringVar(value='##')
    replacer=StringVar(value='%d')
    startfrom=IntVar(value=1)

    def _do_insert(*_):
        pat=pattern.get()
        rep=replacer.get()
        current=startfrom.get()
        res=[]
        for fn in _gtcontent():
            res.append(fn.replace(pat,rep%current))
            current+=1
        fntxt.delete(1.0,END)
        fntxt.insert(END,'\n'.join(res))
        tl.destroy()

    Label(tl,text='占位符').grid(row=0,column=0)
    Entry(tl,textvariable=pattern).grid(row=0,column=1,columnspan=3,sticky='we')
    Label(tl,text='序号格式').grid(row=1,column=0)
    Entry(tl,textvariable=replacer).grid(row=1,column=1,columnspan=3,sticky='we')
    Label(tl,text='起始于').grid(row=2,column=0)
    Entry(tl,textvariable=startfrom,width=6).grid(row=2,column=1)
    Button(tl,text='插入',command=_do_insert).grid(row=2,column=3)

    tl.focus_force()


Button(fe,text='重置文件名',command=init_fn).grid(row=0,column=0)
Button(fe,text='字符替换',command=fn_replace).grid(row=0,column=2)
Button(fe,text='lambda',command=python_replace).grid(row=0,column=3)
Button(fe,text='外部编辑器',command=open_in_npp).grid(row=0,column=4)
Button(fe,text='插入序号',command=replace_with_ind).grid(row=0,column=5)

fntxt_f=Frame(fe)
fntxt_f.grid(row=1,column=0,columnspan=6,sticky='nswe')
fntxt_f.rowconfigure(0,weight=1)
fntxt_f.columnconfigure(0,weight=1)

fntxt=Text(fntxt_f,font='Consolas -12')
fntxt.grid(row=0,column=0,sticky='nswe')
fntxt_sbar=Scrollbar(fntxt_f,orient=VERTICAL,command=fntxt.yview)
fntxt_sbar.grid(row=0,column=1,sticky='ns')
fntxt['yscrollcommand'] = fntxt_sbar.set

##### refactor

def refresh(*_):
    old_fns=_gtfiles()
    new_fns=tuple(_gtcontent())
    if len(old_fns)!=len(new_fns):
        return messagebox.showerror('Renamer','新文件名数量有误')

    for ind in range(len(old_fns)):
        if not os.path.isfile(old_fns[ind]):
            return messagebox.showerror('Rename','要改名的文件不存在：\n\n%s'%old_fns[ind])
        if os.path.exists(new_fns[ind]):
            return messagebox.showerror('Rename','改名的目标已经存在：\n\n%s'%new_fns[ind])

    tree.delete(*tree.get_children())
    for ind in range(len(old_fns)):
        folder,old_fn=os.path.split(old_fns[ind])
        tree.insert('','end',text=folder,values=(old_fn,new_fns[ind]))
    return 'okay'

def do_refactor(*_):
    if refresh()!='okay':
        return

    old_fns=_gtfiles()
    new_fns=tuple(_gtcontent())

    prog['maximum']=len(old_fns)
    prog['value']=0
    for ind in range(len(old_fns)):
        os.rename(old_fns[ind],os.path.join(os.path.split(old_fns[ind])[0],new_fns[ind]))
        prog['value']+=1
        tk.update_idletasks()

    messagebox.showinfo('Renamer','处理完成')
    clear_list()
    fntxt.delete(1.0,END)
    tree.delete(*tree.get_children())

fr.rowconfigure(1,weight=1)
fr.columnconfigure(2,weight=1)

Button(fr,text='刷新状态',command=refresh).grid(row=0,column=0)
Button(fr,text='全部重命名',command=do_refactor).grid(row=0,column=1)
prog=Progressbar(fr,orient=HORIZONTAL,length=200)
prog.grid(row=0,column=2,sticky='we')

tree_f=Frame(fr)
tree_f.grid(row=1,column=0,columnspan=3,sticky='nswe')
tree_f.rowconfigure(0,weight=1)
tree_f.columnconfigure(0,weight=1)

tree=Treeview(tree_f,columns=('oldfn','newfn'))
tree.grid(row=0,column=0,sticky='nswe')
tree_sbar=Scrollbar(tree_f,orient=VERTICAL,command=tree.yview)
tree_sbar.grid(row=0,column=1,sticky='ns')
tree['yscrollcommand'] = tree_sbar.set

tree.column('#0',width=150)
tree.column('oldfn',width=200)
tree.column('newfn',width=200)
tree.heading('#0',text='位置')
tree.heading('oldfn',text='原文件名')
tree.heading('newfn',text='新文件名')

mainloop()