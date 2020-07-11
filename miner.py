from modules import osr
from modules import RandTime
from modules import Mouse
#from modules import Minimap
from modules import Screenshot
import cv2
import numpy as np
import random

# What to mine pass value as string?
mine_this = 'gems'
G = osr.Frame()
#mine_this = 'iron'

def find_mine():
    global mine_this
    mines = {
        'tin1':([0,13,104],[3,73,148]),
        'tin':([0,19,121],[1,30,136]),
        'cooper':([14,135,88],[15,140,169]),
        'iron':([7,138,50],[10,146,85]),
        'gems':([150,223,61],[151,235,169])
    }

    play_window,psx,psy = G.getPlayingScreen('hsv')

    #cv2.imshow('img', play_window)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #mask = cv2.inRange(play_window, np.array(mines['tin'][0]), np.array(mines['tin'][1]))
    #mask = cv2.inRange(play_window, np.array(mines['cooper'][0]), np.array(mines['cooper'][1]))
    mask = cv2.inRange(play_window, np.array(mines[mine_this][0]), np.array(mines[mine_this][1]))

    #cv2.imshow('img', mask)
    #cv2.waitKey(500)
    #cv2.destroyAllWindows()

    kernel = np.ones((10,10), np.uint8)
    closing  =  cv2.morphologyEx(mask.copy(), cv2.MORPH_CLOSE, kernel)

    #cv2.imshow('img', closing)
    #cv2.waitKey(500)
    #cv2.destroyAllWindows()

    contours,_ = cv2.findContours(closing.copy(), 1, 2)
    # adds white rectangle around the mines
    for con in contours:
        x,y,w,h = cv2.boundingRect(con)
        cv2.rectangle(closing,(x,y),(x+w,y+h),(255,255,255),-1)
    #cv2.imshow('closing', closing)
    #cv2.waitKey(500)

    # finds mine mounts
    contours,_ = cv2.findContours(closing.copy(), 1, 2)
    mine_areas = {}
    for con in contours:
        #print("\n###############################")
        print(cv2.contourArea(con))
        area = cv2.contourArea(con)
        if area > 500:
            #print(cv2.contourArea(con))
            M = cv2.moments(con)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            # adds areas to dictionary to call next
            mine_areas[area] = (cx,cy)

    try:
        mines = [key for key in mine_areas.keys()]
        print(type(mines))
        # gets random mine from mine areas
        chosen_mine = random.choice(mines)
    except Exception as e:
        print(e)
        #random_mine = mine_areas[chosen_mine]
    #print(random_mine)
    mine_center_x, mine_center_y = mine_areas[chosen_mine]
    # combine coords with playscreen to make relative
    mine_center_x += psx 
    mine_center_y += psy
    print(mine_center_x)
    print(mine_center_y)

    # adds randomness to coords
    #mine_center_x += random.randint(-5,5)
    #mine_center_y += random.randint(-5,5)

    #Mouse.moveClick(mine_center_x, mine_center_y,1)
    G.hc.click(mine_center_x, mine_center_y)
    #cv2.destroyAllWindows()
    #cv2.imshow('img', mask)
    #cv2.imshow('closing', closing)
    #cv2.waitKey(0)

def main():
    G = osr.Frame()
    #item_n = G.invCount()
    #print("Current itme number is:{}".format(item_n))
    while 1:
        find_mine()
        RandTime.randTime(5,0,0,8,9,9)
        print("Restarting loop...")

main()
