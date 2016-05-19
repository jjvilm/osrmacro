#!/usr/bin/python2
import cv2 #to find template
import numpy as np #needed by cv2
import autopy #for smooth mouse move
import subprocess #needed to access xdotool output
import random #get random time
import time #for sleep
import os #needed to 
from modules import Mouse
from modules import Screenshot
from modules import RS

#Finds an image from the given template.  
cur_dir = os.getcwd()

def find_template(template_file):#pass template to function
    rs_bag, bagx, bagy = RS.get_bag('bag and its coords')
    #cv2.imwrite('debug_bag.png', rs_bag)
    
    #template
    template = cv2.imread(template_file,0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(rs_bag,template,cv2.TM_CCOEFF_NORMED)
    threshold = .9 #default is 8 
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):#goes through each found image
        btmX = pt[0] + w - 10 #pt == top-left coord of template, bottom-right point of of template image
        btmY = pt[1] + h - 10 
        #moving the pt coord of the template a bit to the right, so options menu get brought up
        pt = (pt[0] + 10, pt[1] +10 )
        
        x, y = gen_coords(pt,btmX, btmY, bagx, bagy)#gets random x, y coords relative to RSposition on where to click
        Mouse.moveClick(x,y, 1)#right clicks on given x,y coords
        randTime(0,0,0,0,0,7)
        randTime(0,0,0,0,0,5)
        randTime(0,0,1,0,0,1)

def gen_coords(pt,btmX,btmY, bagx, bagy):
    """Generates random coords of where to click once a template is found inside the bag screenshot"""
    x1 = pt[0] +( bagx + 1) #gets top-left location of able to be right clicked
    y1 = pt[1] +( bagy + 1)

    x2 = btmX +( bagx - 1) #bttm-right location able to be right clicked
    y2 = btmY +( bagy - 1)

    within_x = random.randint(x1,x2)#generates a range of clickable locations 
    within_y = random.randint(y1,y2)
    return within_x, within_y

def randTime(x,y,z,fdigit, sdigit, tdigit):#sleeps in  miliseconds from fdigit.sdigit+tdigit+random
    random.seed()
    n = random.random()
    n = str(n)
    n = n[2:]
    
    fdigit = str(random.randint(x,fdigit))
    sdigit = str(random.randint(y,sdigit))
    tdigit = str(random.randint(z,tdigit))

    
    milisecs = fdigit+'.'+sdigit+tdigit+n
    milisecs = float(milisecs)
    time.sleep(milisecs)

if __name__ == '__main__':
    find_template(cur_dir+'/imgs/grimmyIrit.png')
    #find_template(cur_dir+'/imgs/grimmyGuam.png')
    #find_template(cur_dir+'/imgs/grimmyMarrentil.png')
    #find_template(cur_dir+'/imgs/grimmyTarromin.png')
    #print("Time taken:",timer)
