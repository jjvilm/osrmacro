#!/usr/bin/python2
import cv2 #to find template
import numpy as np #needed by cv2
import autopy #for smooth mouse move

import pyscreenshot #to take screenshot of bag and options menu
import subprocess #needed to access xdotool output
import random #get random time
import time #for sleep
import os #needed to 

### Import my modules
from modules import Mouse
from modules import RandTime 
from modules import Screenshot
from modules import RS

#Finds an image from the given template.  
bag_coord =( ((557,229),(173,253)) )#runescape bag coords as x,y coord, w, h
cur_dir = os.getcwd()
#timer = 0


def find_template(template_file):#pass template to function
    #checks to see wheater to add cur dir or not
    if "/" not in template_file:
        global cur_dir
        template_file = cur_dir+"/imgs/"+template_file
        
    x1, y1 = RS.position() #Get runescapes top-left coords
    
    x1 += 557    #make The Bag's top-left, and btm-right coords
    y1 += 229    #x2,y2 == btm-right coord, width and height
    x2 = x1 + 173 
    y2 = y1 + 253
     
    rs_bag = Screenshot.shoot(x1,y1,x2,y2) #Screenshot taken here, 
    
    #template
    template = cv2.imread(template_file,0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(rs_bag,template,cv2.TM_CCOEFF_NORMED)
    threshold = .8 #default is 8 
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):#goes through each found image
        btmX = pt[0] + w - 5#pt == top-left coord of template, bottom-right point of of template image
        btmY = pt[1] + h - 5
        #moving the pt coord of the template a bit to the right, so options menu get brought up
        pt = (pt[0] + 5, pt[1] + 2)
        
        x, y = gen_coords(pt,btmX, btmY)#gets random x, y coords relative to RSposition on where to click
        moveClick(x,y, 3)#right clicks on given x,y coords
        menu_x, menu_y, menu = RS.getOptionsMenu(x,y)#takes screenshot of options menu and returns the point at Top-left of the menu
        RandTime.randTime(0,0,0,0,0,1)
        
        RS.findOptionClick(x,y,'drop')
        
    RandTime.randTime(2,0,0,2,9,9)
 
def gen_coords(pt,btmX,btmY):
    """Generates random coords of where to click once a template is found inside the bag screenshot"""
    x1 = pt[0] +( bag_coord[0][0] + 1) #gets top-left location of able to be right clicked
    y1 = pt[1] +( bag_coord[0][1] + 1)

    x2 = btmX +( bag_coord[0][0] -1) #bttm-right location able to be right clicked
    y2 = btmY +( bag_coord[0][1] -1)

    within_x = random.randint(x1,x2)#generates a range of clickable locations 
    within_y = random.randint(y1,y2)
    return within_x, within_y

def moveClick(x,y, button=1):#moves to random X,Y of found match of template
    """moves to x,y relative to the RS window"""
    rsx, rsy = RS.position()
    x = rsx + x
    y = rsy + y 
    Mouse.moveTo(x,y)

    autopy.mouse.toggle(True,button)
    RandTime.randTime(0,0,0,0,0,1)
    autopy.mouse.toggle(False,button)
    

if __name__ == '__main__':
    find_template(cur_dir+'/imgs/salmon.png')
    find_template(cur_dir+'/imgs/trout.png')
    find_template(cur_dir+'/imgs/burntfish.png')
    #print("Time taken:",timer)
