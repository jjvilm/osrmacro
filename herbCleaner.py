#!/usr/bin/python2
import cv2 #to find template
import numpy as np #needed by cv2
import autopy #for smooth mouse move

import pyscreenshot #to take screenshot of bag and options menu
import subprocess #needed to access xdotool output
import random #get random time
import time #for sleep
import os #needed to 

#Finds an image from the given template.  
bag_coord =( ((557,229),(173,253)) )#runescape bag coords as x,y coord, w, h
cur_dir = os.getcwd()
timer = 0

#Find given option inside the options menu e.g use,eat,drop,examine,exit,
def findOptionClick(x,y,menu_x,menu_y, menu):#X,Y coords of where it clied in bag
    img_gray = menu #screenshot of menu
    
    #template
    template = cv2.imread(cur_dir+'/imgs/drop.png',0)#0 here means turned gray
    w, h = template.shape[::-1]#Width, height of template image
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = .9 
    loc = np.where( res >= threshold)
    
    for pt in zip(*loc[::-1]):#goes through each found image
        pt_x, pt_y = pt #point of drop found inside the option menu screenshot
        
        x = menu_x + pt_x + (random.randint(5,(w*3))) #generates random x range fr
        y = menu_y + pt_y + (random.randint(5,h-3)) #generats random Y for drop selection
        
        moveTo(x,y)
        
        #autopy.mouse.click()
        #
        autopy.mouse.toggle(True,button)
        randTime(0,0,0,0,0,1)#time between click
        randTime(0,0,0,0,0,0)
        autopy.mouse.toggle(False,button)

        randTime(0,0,0,0,0,1)

def find_template(template_file):#pass template to function
    x1, y1 = rsPosition() #Get runescapes top-left coords
    
    x1 += 557    #make The Bag's top-left, and btm-right coords
    y1 += 229    #x2,y2 == btm-right coord, width and height
    x2 = x1 + 173 
    y2 = y1 + 253
     
    rs_bag = my_screenshot(x1,y1,x2,y2) #Screenshot taken here, 
    
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
        
        x, y = gen_coords(pt,btmX, btmY)#gets random x, y coords relative to RSposition on where to click
        moveClick(x,y, 1)#right clicks on given x,y coords
        randTime(0,0,0,0,0,7)
        randTime(0,0,0,0,0,5)
        randTime(0,0,0,0,0,1)

def gen_coords(pt,btmX,btmY):
    """Generates random coords of where to click once a template is found inside the bag screenshot"""
    x1 = pt[0] +( bag_coord[0][0] + 1) #gets top-left location of able to be right clicked
    y1 = pt[1] +( bag_coord[0][1] + 1)

    x2 = btmX +( bag_coord[0][0] -1) #bttm-right location able to be right clicked
    y2 = btmY +( bag_coord[0][1] -1)

    within_x = random.randint(x1,x2)#generates a range of clickable locations 
    within_y = random.randint(y1,y2)
    return within_x, within_y

def getOptionsMenu(x, y):#X,Y coords of where it right-clicked in bag to bring up the Options Menu
    rs_x, rs_y = rsPosition()#Top-Left coords of where RS window is
    menu_x = rs_x + x        #Adding Rs coords to the options menu to get its location relevant to the window
    menu_y = rs_y + y - 24   #24 here goes up on Y since sometimes screenshot needs to get more of the top Y to find the right option in the options menu. 
    menu_x -= 90#55 default moves x location 70px to top-left of options menu
    menu_x2 = menu_x + 80 #Plus width
    menu_y2 = menu_y + 120 #Plus height 

    menu = my_screenshot(menu_x, menu_y,menu_x2, menu_y2) 
    return menu_x, menu_y, menu

def moveClick(x,y, button):#moves to random X,Y of found match of template
    rsx, rsy = rsPosition()
    x = rsx + x
    y = rsy + y 
    moveTo(x,y)

    #clicks, holds for a random amount of time, then release click
    autopy.mouse.toggle(True,button)
    randTime(0,0,0,0,0,1)
    randTime(0,0,0,0,0,0)
    autopy.mouse.toggle(False,button)

    randTime(0,0,0,0,0,1)

def moveTo(x,y):
    """Move mouse  NOT in a straight line"""
    cur_x, cur_y = autopy.mouse.get_pos() #Gets initial mouse location
    #screen_x, screen_y = autopy.screen.get_size() #gets screen size
   
    while True:
        min_x = min(cur_x, x)#Decides minimun X,Y 
        max_x = max(cur_x, x)#Decides maximum X,Y coords

        min_y = min(cur_y, y)
        max_y = max(cur_y, y)
        
        #find furthest distance of X and Y
        len_x = max_x - min_x
        len_y = max_y - min_y

        overshoot = random.randint(0,40)
        #breaks once it's around +-2 pixels around the target area
        if (len_x) <= 7 and  (len_y) <= 7:
            randTime(0,0,0,0,0,0)
            break
        #checks if current X is higher or lower than target X
        if cur_x > x:#Higher X
            if len_x > 100:
                cur_x -= random.randint(51,99)
            elif len_x <= 10:
                cur_x -= random.randint(1,5)
                if overshoot == 7:
                    cur_x -= random.randint(1,15)
            elif len_x <= 15:
                cur_x -= random.randint(1,5)
            elif len_x <= 25:
                cur_x -= random.randint(1,9)
            elif len_x <= 50:
                cur_x -= random.randint(5,24)
            elif len_x <= 100:
                cur_x -= random.randint(25,55)

        else:#Lower x
            if len_x > 100:
                cur_x += random.randint(51,99)
            elif len_x <= 10:
                cur_x += random.randint(1,5)
                if overshoot == 7:
                    cur_x += random.randint(1,15)
            elif len_x <= 11:
                cur_x += random.randint(1,5)
            elif len_x <= 19:
                cur_x += random.randint(1,9)
            elif len_x <= 50:
                cur_x += random.randint(5,24)
            elif len_x <= 100:
                cur_x += random.randint(25,55)

        #checks if current Y is higher or lower than target Y
        if cur_y > y: # Higher Y
            if len_y > 100:
                cur_y -= random.randint(51,99)
            elif len_y <= 5:
                cur_y -= random.randint(1,3)
                if overshoot == 7:
                    cur_x -= random.randint(1,15)
            elif len_y <= 11:
                cur_y -= random.randint(1,5)
            elif len_y <= 25:
                cur_y -= random.randint(1,9)
            elif len_y <= 50:
                cur_y -= random.randint(5,24)
            elif len_y <= 100:
                cur_y -= random.randint(25,55)
        else: #Lower Y
            if len_y > 100:
                cur_y += random.randint(51,99)
            elif len_y <= 7:
                cur_y += random.randint(1,5)
                if overshoot == 7:
                    cur_x += random.randint(1,15)
            elif len_y <= 11:
                cur_y += random.randint(1,5)
            elif len_y <= 25:
                cur_y += random.randint(1,9)
            elif len_y <= 50:
                cur_y += random.randint(5,25)
            elif len_y <= 100:
                cur_y += random.randint(25,55)
        
        #print("Moving to {0} {1}".format(cur_x, cur_y))
        if overshoot == 7:
            randTime(0,0,0,0,9,9)

        #slows down if closer to target coord
        if (len_x) <= random.randint(1,5) and  (len_y) <= random.randint(1,5):
            randTime(0,0,0,0,9,9)
        else:
            randTime(0,0,0,0,0,1)
            randTime(0,0,0,0,0,1)
            if random.randint(0,3) == 0:
                randTime(0,0,0,0,0,9)
                randTime(0,0,0,0,0,1)

        autopy.mouse.smooth_move(cur_x,cur_y)#moves to generated location



def my_screenshot(x1,y1,x2,y2):#pass top-left coord and btm-right coord of screenshot
    """Takes screenshot at given coordinates as PIL image format,
     then converts to cv2 grayscale image format and returns it"""
    im = pyscreenshot.grab(bbox=(x1,y1,x2,y2)) #X1,Y1,X2,Y2
    im = np.array(im)#converts to numpy array
    cv_img = im.astype(np.uint8)#makes cv2 image object 
    cv_gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)#turns image gray

    return cv_gray

def randTime(x,y,z,fdigit, sdigit, tdigit):#sleeps in  miliseconds from fdigit.sdigit+tdigit+random
    global timer
    random.seed()
    n = random.random()
    n = str(n)
    n = n[2:]
    
    fdigit = str(random.randint(x,fdigit))
    sdigit = str(random.randint(y,sdigit))
    tdigit = str(random.randint(z,tdigit))

    
    milisecs = fdigit+'.'+sdigit+tdigit+n
    milisecs = float(milisecs)
    timer += milisecs
    time.sleep(milisecs)
 


def rsPosition():
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


if __name__ == '__main__':
    find_template(cur_dir+'/imgs/grimmyGuam.png')
    #find_template(cur_dir+'/imgs/grimmyMarrentil.png')
    #find_template(cur_dir+'/imgs/grimmyTarromin.png')
    print("Time taken:",timer)
