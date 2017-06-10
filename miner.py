from modules import RS
from modules import RandTime
from modules import Mouse
from modules import Minimap
import cv2
import numpy as np
import random

# What to mine pass value as string?
#mine_this = 'gems'
mine_this = 'iron'

def find_mine():
    global mine_this
    mines = {
        'tin1':([0,13,104],[3,73,148]),
        'tin':([0,19,121],[1,30,136]),
        'cooper':([14,135,88],[15,140,169]),
        'iron':([7,138,50],[10,146,85]),
        'gems':([150,223,61],[151,235,169])
    }

    play_window,psx,psy = RS.getPlayingScreen()

    #mask = cv2.inRange(play_window, np.array(mines['tin'][0]), np.array(mines['tin'][1]))
    #mask = cv2.inRange(play_window, np.array(mines['cooper'][0]), np.array(mines['cooper'][1]))
    mask = cv2.inRange(play_window, np.array(mines[mine_this][0]), np.array(mines[mine_this][1]))

    kernel = np.ones((20,20), np.uint8)
    closing  =  cv2.morphologyEx(mask.copy(), cv2.MORPH_CLOSE, kernel)

    _,contours,_ = cv2.findContours(closing.copy(), 1, 2)
    # adds white rectangle around the mines
    for con in contours:
        x,y,w,h = cv2.boundingRect(con)
        cv2.rectangle(closing,(x,y),(x+w,y+h),(255,255,255),-1)
    #cv2.imshow('closing', closing)
    #cv2.waitKey(0)

    # finds mine mounts
    _,contours,_ = cv2.findContours(closing.copy(), 1, 2)
    mine_areas = {}
    for con in contours:
        #print("\n###############################")
        #print(cv2.contourArea(con))
        if cv2.contourArea(con) > 500:
            #print(cv2.contourArea(con))
            M = cv2.moments(con)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            # adds areas to dictionary to call next
            mine_areas[cv2.contourArea(con)] = (cx,cy)

    try:
        # gets random mine from mine areas
        random_mine = random.choice(mine_areas.keys())
    except Exception as e:
        #print(e)
        random_mine = mine_areas[mine_areas.keys()[0]]
    #print(random_mine)
    mine_center_x, mine_center_y = mine_areas[random_mine]
    # combine coords with playscreen to make relative
    mine_center_x += psx 
    mine_center_y += psy

    # adds randomness to coords
    mine_center_x += random.randint(-11,11)
    mine_center_y += random.randint(-11,11)

    Mouse.moveClick(mine_center_x, mine_center_y,1)
    #cv2.destroyAllWindows()
    #cv2.imshow('img', mask)
    #cv2.imshow('closing', closing)
    #cv2.waitKey(0)

def main():
    item_n = RS.inventory_counter()
    print("Current itme number is:{}".format(item_n))
    while 1:
        if item_n == 28:
            break
        try:
            #mines the ore
            find_mine()
        except:
            RandTime.randTime(1,0,0,1,0,9)
            continue

        # waits for obtained ore to move on
        safe_counter = 0 #if reaches a X amount safe switches
        while 1:
            current_n_items = RS.inventory_counter()
            # counts to make sure +1 has been added to inv
            if item_n + 1 == current_n_items:
                item_n = current_n_items
                break
            else:
                if safe_counter >=45:
                    break
                RandTime.randTime(0,1,0,0,9,9)
                safe_counter += 1
                continue

    print("Full Inv")
main()

#Minimap.findBankIcon(10,"n")
#RandTime.randTime(4,0,0,6,9,9)
#RS.open_cw_bank()
#while 1:
#    if RS.isBankOpen():
#        RS.depositAll()
#        RS.closeBank()
#        break
#    else:
#        print('not open')
#        RandTime.randTime(0,1,0,0,9,9)
#        continue
#
