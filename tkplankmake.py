#!/usr/bin/python2

from Tkinter import *
import os

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.plankmake = Button(frame, text="Make", fg='white', bg='green', command=self.making)
        self.plankmake.pack()

    def making(self):
        cwd = os.getcwd()
        os.system(cwd+'/plankmake.py')

root = Tk()
app = App(root)
root.mainloop()
