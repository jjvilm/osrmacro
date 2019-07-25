#!/usr/bin/python3
# HerbCleaner.py
import cv2 #to find template
import numpy as np #needed by cv2
# import autopy #for smooth mouse move
# import subprocess #needed to access xdotool output
import random #get random time
import time #for sleep
import os
from modules import Mouse # "Human like" mouse movement
from modules import RandTime
# from modules import setup
from modules import RS # to open bank at Castle Wars
import Herbdat

#Finds an image from the given template.
cur_dir = os.getcwd()
rs = RS.Osr_game()

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

def main(herb_object):
    ## create RS_game object
    global rs
    # var to break out of loop after 3 bank tries
    bankchecking = 0
    n_secs = 1
    while True:
        if bankchecking == 5:
            break
        #open bank
        rs.open_cw_bank()

        #give time for window to open up
        RandTime.randTime(0,0,0,1,9,9)

        #check if bank is NOT open, if not end
        if not rs.isBankOpen():
            bankchecking +=1
            n_secs = n_secs * bankchecking

            time.sleep(n_secs)
            print(f"Waiting {n_secs}secs for bank to be open")
            continue
        # continues with bank open now...
        # resets bankchecking
        bankchecking = 0
        #deposit all
        #if herb_object in inventory
        if not rs.isInvEmpty():
            print("depositing all items, to empty out")
            rs.depositAll()

        #loop makes sure herbs are withdrawn!
        print("Going into main loop")

        while True:
            try:
                herbx,herby = findHerbInBankInv(herb_object)
            except Exception as e:
                print('No more herbs')
                print(e)
                return

            # right-clicks to find options menu
            rs.findOptionClick(herbx,herby,'withdrawAll')
            # Mouse.moveClick(herbx,herby,3)

            # breaks inventory if contains an item
            if not rs.isInvEmpty():
                break
            else:
                # deposits all items from inventory
                rs.depositAll()

        #close bank
        print('closing bank')
        rs.closeBank()
        # start cleaning here
        print(f"Starting to find grimy herbs")
        find_grimmy_herbs_in_inventory(herb_object)

def findHerbInBankInv(herb_object):
    """ returns grimy herb in bank inv with randomized position withing rect"""
    #takes bank screenshot
    bank_screenshot, bankx, banky = rs.getBankWindow('hsv')

    # finds all grimmys first
    low, high = herb_object.herbdic['grimmy']
    low = np.array(low)
    high = np.array(high)
    mask = cv2.inRange(bank_screenshot, low, high)
    ## debug
    #cv2.imshow('img', mask)
    #cv2.waitKey(0)
    ## debug

    # how big in pixels to remove noise
    kernel = np.ones((4,4), np.uint8)

    # removes noise
    #erosion = cv2.erode(mask, kernel, iterations = 1)

    # increases white
    dilation = cv2.dilate(mask, kernel, iterations = 1)

    contours, _ = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # fills in the contours in the mask with a rect
    for con in contours:
        x, y, w, h = cv2.boundingRect(con)
        cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),-1)
    # result of finding only grimmys in the hsv image
    res = cv2.bitwise_and(bank_screenshot,bank_screenshot, mask = mask.copy())
    # finding the passed herb here based on color range
    low, high = herb_object.hsv_range
    low = np.array(low)
    high = np.array(high)
    herb_mask = cv2.inRange(res, low, high)
    ###########
    #debug line
    #cv2.imshow('debug.png', herb_mask)
    #cv2.waitKey(0)
    #return
    ###########

    contours, _ = cv2.findContours(herb_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contour_areas = {}
    # finds center of herb
    for con in contours:
        M = cv2.moments(con)
        #print(M)
        # gets center of object
        x,y = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        break
    if y == 1:
        return
    # makes coords relative to the game window
    x += bankx
    y += banky
    # creates a list from passed ints
    pixels = [i for i in range(-5,5)]
    # randomly adds value from pixels list
    x += random.choice(pixels)
    y += random.choice(pixels)

    # returns coords to right click and get options
    print(f"166:grimmy herb @({x},{y})")
    return x, y

def find_grimmy_herbs_in_inventory(herb_object):
    rs_bag, bagx, bagy = rs.get_bag('bag and its coords', 'hsv')
    # finds all grimmys first
    low, high = herb_object.herbdic['grimmy2']
    low = np.array(low)
    high = np.array(high)
    # applies mask based on above values
    mask = cv2.inRange(rs_bag, low, high)

    kernel = np.ones((5,5), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations = 1)

    # contours of all grimys found
    contours, _ = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # adds a white rectangle to all grimmys
    for con in contours:
        x, y, w, h = cv2.boundingRect(con)
        cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),-1)
    # goes through each item and clicks it
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    items_coords = []
    row = []
    col = 0
    for con in contours[::-1]:
        M = cv2.moments(con)
        #print(M)
        # gets center of object
        x,y = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        # makes coords relative to the window
        x += bagx
        y += bagy
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
    herb = Herbdat.Herb()
    main(herb)
