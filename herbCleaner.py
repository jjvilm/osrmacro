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
import Herbdat

#Finds an image from the given template.  
cur_dir = os.getcwd()
RSX,RSY = RS.position()

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

def main(herb_name):
    # var to break out of loop after 3 bank tries
    bankchecking = 0
    n_secs = 1
    while True:
        if bankchecking == 5:
            break
        #open bank
        RS.open_cw_bank()

        #give time for window to open up
        time.sleep(1.2)

        #check if bank is open, if not end
        if not RS.isBankOpen():
            bankchecking +=1 
            n_secs = n_secs * bankchecking

            time.sleep(n_secs)
            continue

        # resets bankchecking
        bankchecking = 0
        #deposit all
        #if herb_name in inventory
        if not RS.isInvEmpty():
            RS.depositAll()
        
        #loop makes sure herbs are withdrawn!
        while True:
            try:
                herbx,herby = findherb(herb_name)
            except Exception as e:
                print('No more herbs')
                print(e)
                return
            Mouse.moveClick(herbx,herby,3)

            # removes RS coords since added back in in findOptionClick
            herbx -= RSX
            herby -= RSY
            RS.findOptionClick(herbx,herby,'withdrawAll')

            time.sleep(.9)
            randTime(0,0,0,0,0,9)
            # breaks when items are taken out into inventory
            if not RS.isInvEmpty():
                break
            else:
                # deposits all items from inventory
                x,y = Mouse.genCoords(RSX+13,RSY+60,RSX+500,RSY+352)
                Mouse.moveTo(x,y)

        #close bank
        RS.closeBank()
        find_grimmy_herbs_in_inventory()

def findherb(herb_name):
    #takes bank screenshot
    bank_screenshot, bankx, banky = RS.getBankWindow('hsv')

    # finds all grimmys first
    low, high = Herbdat.herb('grimmy')
    low = np.array(low)
    high = np.array(high)
    mask = cv2.inRange(bank_screenshot, low, high)

    # how big in pixels to remove noise
    kernel = np.ones((5,5), np.uint8)

    # removes noise
    #erosion = cv2.erode(mask, kernel, iterations = 1)

    # increases white 
    dilation = cv2.dilate(mask, kernel, iterations = 1)

    _, contours, _ = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # fills in the contours in the mask with a rect
    for con in contours:
        x, y, w, h = cv2.boundingRect(con)
        cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),-1)
    # result of finding only grimmys in the hsv image
    res = cv2.bitwise_and(bank_screenshot,bank_screenshot, mask = mask.copy())
    # finding the passed herb here based on color range 
    low, high = Herbdat.herb(herb_name)
    low = np.array(low)
    high = np.array(high)
    herb_mask = cv2.inRange(res, low, high)
    ###########
    #debug line
    #cv2.imshow('debug.png', herb_mask)
    #cv2.waitKey(0)
    #return
    ###########

    _, contours, _ = cv2.findContours(herb_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_areas = {}
    # finds center of herb
    for con in contours:
        M = cv2.moments(con)
        #print(M)
        # gets center of object
        x,y = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        break
    if y == 1:
        return 
    # makes coords relative to the window
    x += RSX + bankx
    y += RSY + banky
    # creates a list from -20 to 20
    pixels = [i for i in range(-15,15)]
    # randomly adds value from pixels list
    x += random.choice(pixels)
    y += random.choice(pixels)

    # returns coords to right click and get options
    return x, y 

def find_grimmy_herbs_in_inventory():
    rs_bag, bagx, bagy = RS.get_bag('bag and its coords', 'hsv')
    # finds all grimmys first
    low, high = Herbdat.herb('grimmy2')
    low = np.array(low)
    high = np.array(high)
    # applies mask based on above values
    mask = cv2.inRange(rs_bag, low, high)

    kernel = np.ones((5,5), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations = 1)

    _, contours, _ = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # adds a white rectangle to all grimmys
    for con in contours:
        x, y, w, h = cv2.boundingRect(con)
        cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),-1)
    # goes through each item and clicks it
    _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    items_coords = []
    row = []
    col = 0
    for con in contours[::-1]:
        M = cv2.moments(con)
        #print(M)
        # gets center of object
        x,y = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        # makes coords relative to the window
        x += RSX + bagx
        y += RSY + bagy 
        # creates a list from -20 to 20
        pixels = [i for i in range(-10,10)]
        # randomly adds value from pixels list
        x += random.choice(pixels)
        y += random.choice(pixels)

        row.append((x,y))

        col += 1
        # appends the row 
        if col == 4:
            items_coords.append(row)
            row = []
            col = 0
    # makes sure to clean the last 3 herbs in bank
    if len(contours) <= 3:
        items_coords.append(row)
    
    # clicks on herbs in a zigzag pattern
    row = 2
    for rows in items_coords:
        # first row gets clicked from left to right
        if row % 2 == 0:
            for coords in rows:
                x, y = coords
                Mouse.moveClick(x,y, 1)#right clicks on given x,y coords
                randTime(0,0,0,0,0,7)
                randTime(0,0,0,0,0,5)
                randTime(0,0,1,0,0,1)

            row += 1
            continue
        else:
        # inverts this row, from right to left
            for coords in rows[::-1]:
                x, y = coords
                Mouse.moveClick(x,y, 1)#right clicks on given x,y coords
                randTime(0,0,0,0,0,7)
                randTime(0,0,0,0,0,5)
                randTime(0,0,1,0,0,1)
        row += 1

if __name__ == '__main__':
    #answer = raw_input("Shutdown after done? [Y]/[N]\n")
    main(Herbdat.chooseHerbs())
    #if answer == 'y':
    #    os.system('sudo shutdown now')
