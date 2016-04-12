#!/usr/bin/python2

from Tkinter import *
import os


cwd = os.getcwd()

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.plankmake = Button(frame,
                text="Make",
                fg='white',
                bg='green',
                command=self.making)
        self.plankmake.pack()

        self.rezise_btn = Button(frame,
                text="Rezise RS",
                fg="black",
                bg='yellow',
                command=self.resize_rs)
        self.rezise_btn.pack()

        self.center_btn = Button(frame, 
                text="center",
                fg='black',
                bg='teal',
                command=self.centering)

    def making(self):
        cwd = os.getcwd()
        os.system(cwd+'/plankmake.py')
    def resize_rs(self):
        os.system('xdotool search old windowsize --sync 767 564')

    def centering(self):
        os.system(cwd+'/setup.py')
root = Tk()
app = App(root)
root.mainloop()
