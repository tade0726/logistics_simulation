
from tkinter import *

root = Tk()

def hello():
    print ("hello!")

menu_bar = Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menu_bar, tearoff=0)
# filemenu.add_command(label="Open", command=hello)
# filemenu.add_command(label="Save", command=hello)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(
    {
        'label': "Copy",
        'command': hello
    }
)
# edit_menu.add_command(label="Copy", command=hello)
# edit_menu.add_command(label="Paste", command=hello)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# helpmenu = Menu(menubar, tearoff=0)
# helpmenu.add_command(label="About", command=hello)
# menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menu_bar)

root.mainloop()