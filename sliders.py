#!/user/bin/python2
from Tkinter import *
from PIL import Image
from PIL import ImageTk
#import tkFileDialog
import time
import cv2
import numpy as np
once = True

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.grid()
        root.title("Sliders")

        self.rlbl = Label(text="Red", fg='red')
        self.rlbl.grid(row=2)
        self.lower_r = Scale(master, label='Low',from_=0, to=255, length=1000,orient=HORIZONTAL, command=self.show_changes)
        self.lower_r.grid(row=3)

        self.upper_r = Scale(master,label='High', from_=0, to=255, length=1000,orient=HORIZONTAL, command=self.show_changes)
        self.upper_r.set(255)
        self.upper_r.grid(row=4)
###########################################################################################################
        self.rlbl = Label(text="Green", fg='green')
        self.rlbl.grid(row=5)
        self.lower_g = Scale(master, from_=0, to=255, length=1000,orient=HORIZONTAL, command=self.show_changes)
        self.lower_g.grid(row=6)

        self.upper_g = Scale(master, from_=0, to=255, length=1000,orient=HORIZONTAL, command=self.show_changes)
        self.upper_g.set(255)
        self.upper_g.grid(row=7)


###########################################################################################################
        self.rlbl = Label(text="Blue", fg='Blue')
        self.rlbl.grid(row=8)
        self.lower_b = Scale(master, from_=0, to=255, length=1000,orient=HORIZONTAL, command=self.show_changes)
        self.lower_b.grid(row=9)

        self.upper_b = Scale(master, from_=0, to=255, length=1000,orient=HORIZONTAL, command=self.show_changes)
        self.upper_b.set(255)
        self.upper_b.grid(row=10)
###########################################################################################################
# buttons
        self.reset_btn = Button(text='Reset', command=self.reset_values)
        self.reset_btn.grid(row=1,column=1)

        self.save_btn = Button(text='Save', command=self.save_values)
        self.save_btn.grid(row=2, column=1)
##########################################################################################################

        self.imglbl = Label(text="HSV",image=None)
        self.imglbl.grid(row=0, column=0)

        self.imglbl2 = Label(text='Original',image=None)
        self.imglbl2.grid(row=0, column=1)



    def show_changes(self, *args):
        global once
        # gets the values from the sliders
        # low blue, green, red
        lb = self.lower_b.get()
        lg = self.lower_g.get()
        lr = self.lower_r.get()
        # gets upper values from sliders
        ub = self.upper_b.get()
        ug = self.upper_g.get()
        ur = self.upper_r.get()

        if lb > ub or lg > ug or lr > ur:
            return 0

        
        img_a = cv2.imread('objects.png',-1)
        if once: 
            # OpenCV represetns images in BGR order; however PIL represents
            # images in RGB order, so we need to swap the channels
            imgO = cv2.cvtColor(img_a, cv2.COLOR_BGR2RGB)
            
            # convert the images to PIL format
            imgO = Image.fromarray(imgO)
            # convert to ImageTk format
            imgO = ImageTk.PhotoImage(imgO)
            # update the original image label
            self.imglbl2.configure(image=imgO)
            # Keeping a reference! b/ need to! 
            self.imglbl2.image = imgO
            once = False


        
        #converts image to HSV 
        img = cv2.cvtColor(img_a, cv2.COLOR_BGR2HSV)
        #converts image to an array usable for open cv2
        img = np.array(img)
        
        # sets the lower and uppper values for the mask
        # opencv reads colors in that order bgr
        lower_color = np.array([lb,lg,lr]) 
        upper_color= np.array([ub,ug,ur])
        #creates the mask and result
        mask = cv2.inRange(img_a, lower_color, upper_color)
        #res = cv2.bitwise_and(img, img, mask=mask)

        # converting to RGB format
        #mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
        # converting to PIL format
        mask = Image.fromarray(mask)
        # convertint to ImageTk format
        mask = ImageTk.PhotoImage(mask)

        self.imglbl.configure(image=mask)
        # adding a reference to the image to Prevent python's garbage collection from deleting it
        self.imglbl.image = mask

        #displays the image
        #cv2.imshow('img', mask)
        # waits for 'esc' to be pressed(or a key)
        #cv2.waitKey(0)
        # does not actually close the window as it shoudl
        #cv2.destroyAllWindows()
    def reset_values(self):
        self.lower_r.set(0)
        self.lower_g.set(0)
        self.lower_b.set(0)

        self.upper_r.set(255)
        self.upper_g.set(255)
        self.upper_b.set(255)

    def save_values(self):
        print("Low = [{},{},{}]".format(self.lower_b.get(), self.lower_g.get(), self.lower_r.get()))
        print("High= [{},{},{}]".format(self.upper_b.get(), self.upper_g.get(), self.upper_r.get()))


root = Tk()
app = App(root)
root.mainloop()
