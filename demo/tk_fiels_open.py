#!/usr/bin/env python

from tkinter import *
from tkinter.filedialog import askopenfilename


class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.button = Button(frame, text="QUIT", command=frame.quit)
        self.button.pack(side=BOTTOM)

        self.text = Text(frame)
        self.text.pack(side=TOP)

        self.choosen = askopenfilename(initialdir='~')
        self.text.insert(END, open(self.choosen).read())

root = Tk()
app = App(root)
root.mainloop()