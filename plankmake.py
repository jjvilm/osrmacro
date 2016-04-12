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
bag_coord =( ((549,225),(189,261)) )#runescape bag coords as x,y coord, w, h
cur_dir = os.getcwd()
timer = 0

def find_template(template_file):#pass template to function

    #Get runescapes top-left coords
    rs_x, rs_y = rsPosition() 

    #moves to spellbook and clicks it
    moveClick(744 + random.randint(0,7), 205 + random.randint(0,7)  )
    
    #moves to spell and clicks
    moveClick((random.randint(560,567)),(random.randint(386,399)))

    time.sleep(.1)

    #makes RECT for screenshot
    x1 = rs_x + 549
    y1 = rs_y + 225
    x2 = x1 + 189
    y2 = y1 + 261

    #Takes screenshot of inventory
    rs_bag = my_screenshot(x1,y1,x2,y2) #Screenshot taken here, 
    
    #Starts Template search
    template = cv2.imread(template_file,0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(rs_bag,template,cv2.TM_CCOEFF_NORMED)
    threshold = .9 #default is 8 
    loc = np.where( res >= threshold)
    iteration = 1
    for pt in zip(*loc[::-1]):#goes through each found image
        if iteration <= 25:
            print(iteration)
            btmX = pt[0] + w - 10#pt == top-left coord of template, bottom-right point of of template image
            btmY = pt[1] + h - 10
            #moving the pt coord of the template a bit to the right, so options menu get brought up
            pt = (pt[0] + 7, pt[1] + 7)
            
            #generates random coordinates withing clickable limits for x,y
            x, y = gen_coords(pt,btmX, btmY)#gets random x, y coords relative to RSposition on where to click

            #moves to log and clicks it
            moveTo(x,y)
            autopy.mouse.click()
            randTime(0,0,0,0,0,5)

            #moves to spell "plank make"
            moveTo(rs_x+random.randint(561,567),rs_y+random.randint(386,394) )

            if iteration <= 16:
                randTime(0,9,9,0,9,9)
            else:
                if iteration == 17:
                    randTime(0,9,9,0,9,9)#waits a bit longer if on 17 to give time to move
                randTime(0,9,9,0,9,9)
                randTime(0,0,1,0,0,9)

            #Clicks spell "plank make" only if less than 25 iterations
            if iteration < 25:
                autopy.mouse.click()

            iteration += 1

def gen_coords(pt,btmX,btmY):
    """Generates random coords of where to click once a template is found inside the bag screenshot"""
    x1 = pt[0] +( bag_coord[0][0] + 1) #gets top-left location of able to be right clicked
    y1 = pt[1] +( bag_coord[0][1] + 1)

    x2 = btmX +( bag_coord[0][0] -1) #bttm-right location able to be right clicked
    y2 = btmY +( bag_coord[0][1] -1)

    within_x = random.randint(x1,x2)#generates a range of clickable locations 
    within_y = random.randint(y1,y2)
    return within_x, within_y

def moveClick(x,y):#moves to random X,Y of found match of template
    """No need to add RSpostion to the passed coordinates x, y"""
    rsx, rsy = rsPosition()
    x = rsx + x
    y = rsy + y 
    moveTo(x,y)
    autopy.mouse.click()

def moveTo(x,y):
    """Move mouse  NOT in a straight line"""
    cur_x, cur_y = autopy.mouse.get_pos() #Gets initial mouse location

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
        if (len_x) <= 3 and  (len_y) <= 3:
            break
        #checks if current X is higher or lower than target X
        if cur_x > x:#Higher X
            if len_x > 100:
                cur_x -= random.randint(51,99)
            elif len_x <= 7:
                cur_x -= random.randint(1,3)
                if overshoot == 7:
                    cur_x -= random.randint(5,15)
            elif len_x <= 19:
                cur_x -= random.randint(1,9)
            elif len_x <= 50:
                cur_x -= random.randint(5,24)
            elif len_x <= 100:
                cur_x -= random.randint(25,55)

        else:#Lower x
            if len_x > 100:
                cur_x += random.randint(51,99)
            elif len_x <= 7:
                cur_x += random.randint(1,3)
                if overshoot == 7:
                    cur_x += random.randint(5,15)
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
            elif len_y <= 7:
                cur_y -= random.randint(1,3)
                if overshoot == 7:
                    cur_x -= random.randint(5,15)
            elif len_y <= 19:
                cur_y -= random.randint(1,9)
            elif len_y <= 50:
                cur_y -= random.randint(5,24)
            elif len_y <= 100:
                cur_y -= random.randint(25,55)
        else: #Lower Y
            if len_y > 100:
                cur_y += random.randint(51,99)
            elif len_y <= 7:
                cur_y += random.randint(1,3)
                if overshoot == 7:
                    cur_x += random.randint(5,15)
            elif len_y <= 19:
                cur_y += random.randint(1,9)
            elif len_y <= 50:
                cur_y += random.randint(5,25)
            elif len_y <= 100:
                cur_y += random.randint(25,55)
        
        #print("Moving to {0} {1}".format(cur_x, cur_y))
        if overshoot == 7:
            randTime(0,0,1,0,1,9)

        #slows down if closer to target coord
        if (len_x) <= random.randint(1,5) and  (len_y) <= random.randint(1,5):
            randTime(0,0,0,0,1,9)
        else:
            randTime(0,0,0,0,0,2)
            if random.randint(0,3) == 0:
                randTime(0,0,0,0,0,3)

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
    find_template(cur_dir+'/imgs/mahagonylog.png')
    print("Done")
    print("Time taken:",timer)
