import cv2
import numpy as np
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
from modules import Match

bag_coord =( ((557,229),(173,253)) )#runescape bag coords as x,y coord, w, h
cur_dir = os.getcwd()

def find_template(template_file, option=None):#pass template to function
#option == to option in menu when righ-clicked on item
    #checks to see wheater to add cur dir or not
    if "/" not in template_file:
        global cur_dir
        template_file = cur_dir+"/imgs/"+template_file
        
    rs_bag = RS.get_bag() #Screenshot taken here, 
    
    #loc == coordinates found in match
    loc = Match.this(rs_bag, template_file)
    for pt in zip(*loc[::-1]):#goes through each found image
	btmX = pt[0] + w - 5#pt == top-left coord of template, bottom-right point of of template image
        btmY = pt[1] + h - 5
        #moving the pt coord of the template a bit to the right, so options menu get brought up
        pt = (pt[0] + 5, pt[1] + 2)
        
        x, y = gen_coords(pt,btmX, btmY)#gets random x, y coords relative to RSposition on where to click
	if option == 'click':
	    moveClick(x,y, 1)#right clicks on given x,y coords
	else:
	    moveClick(x,y, 3)#right clicks on given x,y coords
	    menu_x, menu_y, menu = RS.getOptionsMenu(x,y)#takes screenshot of options menu and returns the point at Top-left of the menu
	    RandTime.randTime(0,0,0,0,0,1)
	    
	    RS.findOptionClick(x,y, menu_x, menu_y, menu, option)
	break
        
	 
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
    RandTime.randTime(0,0,0,0,0,0)
    autopy.mouse.toggle(False,button)
    
def moveToFletchingOptions():
    x, y = RS.position() #gets position of RS window
    x, y = gen_coords( (23,397), 167,469) #get random coors within template
    Mouse.moveClick(x,y,3) #right-clicks on short bow
    RS.getOptions NOT DONE
    then take pic, find option "make x", click it.  type 99, press enter
    
    
    
    
    
if __name__ == '__main__':
    find_tempalte('knife.png','click')
    find_template('MapleLog.png','click')
    #print("Time taken:",timer)

