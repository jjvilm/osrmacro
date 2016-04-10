#!/usr/bin/python2
from Tkinter import *
import os


class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.dropbtn = Button(frame, 
                text= "DROP", fg='red',
                command= self.dropem)
        self.dropbtn.pack(side=LEFT)

        self.loginbtn = Button(frame, text="Log In", fg='blue', command=self.login)
        self.loginbtn.pack()


    def dropem(self):
        cwd = os.getcwd()
        os.system(cwd+'/findndrop.py')

    def login(self):
        cwd = os.getcwd()
        os.system(cwd+'/user_login.py')
        
root = Tk()
app = App(root)
root.mainloop()

