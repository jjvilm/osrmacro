#!/usr/bin/python2
import cv2
import numpy as np
import autopy
import subprocess
import os
import random

#### My Modules 
import Screenshot
import Mouse
import RandTime





def position():
    """Finds Old Runescape Window by name "old", returns the top-left coord as x,y
	To make sure, the bag, and options menu coordinates are relevant to the window"""
    rs_coords = subprocess.check_output(['xdotool','search','--name', 'Old','getwindowgeometry'])
    rs_coords = str(rs_coords)
    
    ##Find the ":" and "," to get the coordinates after them 
    first_occurance = rs_coords.find(":")#x, y coordinates extracted from window geometry
    sec_occurance = rs_coords.find(",")
    thr_occurance = rs_coords.find("(")
    x = rs_coords[first_occurance+1: sec_occurance] #gets x coordinate
    y = rs_coords[sec_occurance+1:thr_occurance] #gets y coordinate
    
    ##change from str to int
    return int(x), int(y)
    
def getOptionsMenu(x, y):#X,Y coords of where it right-clicked in bag to bring up the Options Menu
    """Returns"""
    #Top-Left coords of where RS window is
    rs_x, rs_y = position()
    
    #Adding Rs coords to the options menu to get its location relevant to the window
    #24 here goes up on Y since sometimes screenshot needs to get more of the 
    #top Y to find the right option in the options menu.  
    menu_x = rs_x + x
    menu_y = rs_y + y - 24   
    menu_x -= 90#55 default moves x location 70px to top-left of options menu
    menu_x2 = menu_x + 80 #Plus width
    menu_y2 = menu_y + 120 #Plus height 
    
    #takes screenshot here
    menu = Screenshot.shoot(menu_x, menu_y,menu_x2, menu_y2) 
    
    return menu_x, menu_y, menu
    
def findOptionClick(x,y,menu_x,menu_y, menu, option):#X,Y coords of where it clied in bag
    #get base directory osrmacro
    cur_dir = os.getcwd()
    
    #occurance = cur_dir.rfind("/") #finds the last "/", returns its index
    #cur_dir = cur_dir[:occurance+1] #'/home/user/osrmacro/'
    
    img_gray = menu #screenshot of menu
    
    #template
    template = cv2.imread(cur_dir+'/imgs/'+option+'.png',0)#0 here means turned gray
    
    w, h = template.shape[::-1]#Width, height of template image
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = .8 
    loc = np.where( res >= threshold)
    
    for pt in zip(*loc[::-1]):#goes through each found image
        pt_x, pt_y = pt #point of drop found inside the option menu screenshot
        
        x = menu_x + pt_x + (random.randint(5,(w*3))) #generates random x range fr
        y = menu_y + pt_y + (random.randint(5,h-3)) #generats random Y for drop selection
        
        Mouse.moveTo(x,y)
        
        autopy.mouse.click()
        RandTime.randTime(0,0,0,0,0,9)
    
