from modules import RS
from modules import RandTime
from modules import Mouse
from modules import Minimap
import cv2
import numpy as np
import random

def find_mine():
    mines = {
        'tin':([0,13,104],[3,73,148])
    }

    play_window,psx,psy = RS.getPlayingScreen()

    mask = cv2.inRange(play_window, np.array(mines['tin'][0]), np.array(mines['tin'][1]))

    _,contours,_ = cv2.findContours(mask.copy(), 1, 2)

    kernel = np.ones((20,20), np.uint8)

    closing  =  cv2.morphologyEx(mask.copy(), cv2.MORPH_CLOSE, kernel)

    mine_areas = {}
    for con in contours:
        if cv2.contourArea(con) > 300:
            #print(cv2.contourArea(con))
            M = cv2.moments(con)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            # adds areas to dictionary to call next
            mine_areas[cv2.contourArea(con)] = (cx,cy)

    # gets random mine from mine areas
    random_mine = random.choice(mine_areas.keys())
    #print(random_mine)
    mine_center_x, mine_center_y = mine_areas[random_mine]
    # combine coords with playscreen to make relative
    mine_center_x += psx 
    mine_center_y += psy

    # adds randomness to coords
    mine_center_x += random.randint(-15,15)
    mine_center_y += random.randint(-15,15)

    Mouse.moveClick(mine_center_x, mine_center_y,1)
    #cv2.imshow('img', mask)
    #cv2.imshow('closing', closing)
    #cv2.waitKey(0)


while RS.inventory_counter() < 28:
    find_mine()
    RandTime.randTime(2,0,0,5,9,9)

Minimap.findBankIcon()
RandTime.randTime(3,0,0,5,9,9)
RS.open_cw_bank()

