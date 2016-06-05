#!/user/bin/python2
from Tkinter import *
import time
import cv2
import numpy as np

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.grid()
        root.title("Sliders")

        self.lower_r = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.lower_r.pack()

        self.lower_g = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.lower_g.pack()

        self.lower_b = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.lower_b.pack()

        self.upper_r = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.upper_r.pack()

        self.upper_g = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.upper_g.pack()

        self.upper_b = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.upper_b.pack()

        self.show_btn = Button(master, text="show", command=self.show_changes)
        self.show_btn.pack()

    def show_changes(self):
        img_a = cv2.imread('objects.jpg',-1)
        
        #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.cvtColor(img_a, cv2.COLOR_BGR2HSV)
        img = np.array(img)

        lb = self.lower_b.get()
        lg = self.lower_g.get()
        lr = self.lower_r.get()

        ub = self.upper_b.get()
        ug = self.upper_g.get()
        ur = self.upper_r.get()
        



        lower_color = np.array([lb,lg,lr]) 
        upper_color= np.array([ub,ug,ur])
        print(lower_color)
        print(upper_color)
        
        mask = cv2.inRange(img_a, lower_color, upper_color)
        mas2 = cv2.inRange(img_a, lower_color, upper_color)

        res = cv2.bitwise_and(img, img, mask=mask)

        cv2.imshow('img', mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
            






root = Tk()
app = App(root)
root.mainloop()
