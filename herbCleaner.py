#!/usr/bin/python2
import cv2 #to find template
import numpy as np #needed by cv2
import autopy #for smooth mouse move
import subprocess #needed to access xdotool output
import random #get random time
import time #for sleep
import os 
from modules import Mouse # "Human like" mouse movement
from modules import RS # to open bank at Castle Wars

#Finds an image from the given template.  
cur_dir = os.getcwd()
RSX,RSY = RS.position()

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

def main():
    # var to break out of loop after 3 bank tries
    bankchecking = 0
    while True:
        if bankchecking == 3:
            break
        #open bank
        RS.open_cw_bank()

        #give time for window to open up
        time.sleep(1.2)

        #check if bank is open, if not end
        if not RS.isBankOpen():
            bankchecking +=1 
            time.sleep(2)
            continue

        # resets bankchecking
        bankchecking = 0
        #deposit all
        #if herb_name in inventory
        #if RS.countItemInInv('grimmyGuam.png', 1):
        if not RS.isInvEmpty():
            RS.depositAll()
        
        #loop makes sure herbs are withdrawn!
        while True:
            herbx,herby = findherb('irit')
            Mouse.moveClick(herbx,herby,3)

            # removes RS coords since added back in in findOptionClick
            herbx -= RSX
            herby -= RSY
            RS.findOptionClick(herbx,herby,'withdrawAll')

            time.sleep(.9)
            randTime(0,0,0,0,0,9)
            if not RS.isInvEmpty():
                break
            else:
                # deposits all items from inventory
                x,y = Mouse.genCoords(RSX+13,RSY+60,RSX+500,RSY+352)
                Mouse.moveTo(x,y)

        #close bank
        RS.closeBank()
        #clean herbs
        #find_template(cur_dir+'/imgs/grimmyGuam.png')
        find_template(cur_dir+'/imgs/grimmyIrit.png')
        #find_template(cur_dir+'/imgs/grimmyMarrentil.png')
        #find_template(cur_dir+'/imgs/grimmyTarromin.png')
        #print("Time taken:",timer)

def findherb(herb_name):
    import Herbdat
    bank_screenshot, bankx, banky = RS.getBankWindow('hsv')
    # finds all grimmys first
    low, high = Herbdat.herb('grimmy')
    low = np.array(low)
    high = np.array(high)
    mask = cv2.inRange(bank_screenshot, low, high)

    kernel = np.ones((5,5), np.uint8)
    # removes noise
    #erosion = cv2.erode(mask, kernel, iterations = 1)
    # increases white 
    dilation = cv2.dilate(mask, kernel, iterations = 1)

    contours, _ = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #####################################3
    for con in contours:
        x, y, w, h = cv2.boundingRect(con)
        cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),-1)
    # result of finding only grimmys
    res = cv2.bitwise_and(bank_screenshot,bank_screenshot, mask = mask.copy())
    # finding the passed herb here based on color range 
    low, high = Herbdat.herb(herb_name)
    low = np.array(low)
    high = np.array(high)
    mask = cv2.inRange(res, low, high)
    #################################
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_areas = {}
    for con in contours:
        M = cv2.moments(con)
        #print(M)
        # gets center of object
        x,y = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        break
    # makes coords relative to the window
    x += RSX + bankx
    y += RSY + banky
    # creates a list from -20 to 20
    pixels = [i for i in range(-20,20)]
    # randomly adds value from pixels list
    x += random.choice(pixels)
    y += random.choice(pixels)

    # returns coords to right click and get options
    return x, y 

if __name__ == '__main__':
    main()
    #findherb('irit')
