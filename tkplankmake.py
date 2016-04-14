#!/usr/bin/python2

from Tkinter import *
import os


cwd = os.getcwd()

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.dropper_btn = Button(frame, 
                text="DROP",
                fg='red',
                bg='orange',
                command=self.dropper)
        self.dropper_btn.pack()

        self.herbClean_btn = Button(frame, 
                text="Clean Herb",
                fg='white',
                bg='green',
                command=self.herbClean)
        self.herbClean_btn.pack()

        self.plankmake = Button(frame,
                text="Make Plank",
                fg='white',
                bg='#65453F',
                command=self.making)
        self.plankmake.pack()

        self.center_btn = Button(frame, 
                text="Center RS",
                fg='black',
                bg='yellow',
                command=self.centering)
        self.center_btn.pack()

        self.rezise_btn = Button(frame,
                text="Resize RS",
                fg="black",
                bg='yellow',
                command=self.resize_rs)
        self.rezise_btn.pack()


    def making(self):
        cwd = os.getcwd()
        os.system(cwd+'/plankmake.py')
    def resize_rs(self):
        os.system('xdotool search --name old windowsize --sync 767 564')

    def centering(self):
        os.system(cwd+'/setup.py')
    def herbClean(self):
        os.system(cwd+'/herbCleaner.py')
    def dropper(self):
        os.system(cwd+'/findndrop.py')
root = Tk()
root.title('Various Macros')
app = App(root)
root.mainloop()
