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

        self.rlbl = Label(text="Red", fg='red')
        self.rlbl.grid()
        self.lower_r = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.lower_r.grid()

        self.upper_r = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.upper_r.grid()

        self.rlbl = Label(text="Green", fg='green')
        self.rlbl.grid()
        self.lower_g = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.lower_g.grid()

        self.upper_g = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.upper_g.grid()

        self.rlbl = Label(text="Blue", fg='Blue')
        self.rlbl.grid()
        self.lower_b = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.lower_b.grid()

        self.upper_b = Scale(master, from_=0, to=255, orient=HORIZONTAL)
        self.upper_b.grid()
        # shows the image
        self.show_btn = Button(master, text="show", command=self.show_changes)
        self.show_btn.grid()

    def show_changes(self):
        img_a = cv2.imread('objects.png',-1)
        
        #converts image to HSV 
        img = cv2.cvtColor(img_a, cv2.COLOR_BGR2HSV)
        #converts image to an array usable for open cv2
        img = np.array(img)
        # gets the values from the sliders
        # low blue, green, red
        lb = self.lower_b.get()
        lg = self.lower_g.get()
        lr = self.lower_r.get()
        # gets upper values from sliders
        ub = self.upper_b.get()
        ug = self.upper_g.get()
        ur = self.upper_r.get()
        


        # sets the lower and uppper values for the mask
        
        lower_color = np.array([lb,lg,lr]) 
        upper_color= np.array([ub,ug,ur])
        #creates the mask and result
        mask = cv2.inRange(img_a, lower_color, upper_color)
        res = cv2.bitwise_and(img, img, mask=mask)
        #displays the image
        cv2.imshow('img', mask)
        # waits for 'esc' to be pressed(or a key)
        cv2.waitKey(0)
        # does not actually close the window as it shoudl
        #cv2.destroyAllWindows()
            






root = Tk()
app = App(root)
root.mainloop()
