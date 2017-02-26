from modules import RS
from modules import Mouse
from modules import RandTime
from modules import Health
import numpy as np
import cv2
import time

def find_ham_guard():
    import random
    try:
        ps, psx, psy = RS.getPlayingScreen()

        lower_pink = np.array([154,0,0])
        upper_pink = np.array([160,255,255])

        mask = cv2.inRange(ps, lower_pink, upper_pink)


        _, contours, _ = cv2.findContours(mask.copy(), 1,2)

        for cnt in contours:
            if cv2.contourArea(cnt) <= 1:
                continue
            #print("Area: {}".format(cv2.contourArea(cnt)))
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cx += psx
            cy += psy

            cx += random.randint(-20,20)
            cy += random.randint(-20,20)

            # Find bouding box coords

            Mouse.moveClick(cx,cy, 3)
            break

        RS.findOptionClick(cx,cy, 'pickpocket')
    except Exception as e:
        print(e)
        #cv2.imshow('img', mask)
        #cv2.waitKey(0)

def find_yellow_birds():
    ps, psx, psy = RS.getPlayingScreen()

    lower_pink = np.array([28,197,168])
    upper_pink = np.array([29,234,239])

    mask = cv2.inRange(ps, lower_pink, upper_pink)

    #cv2.imshow('img', mask)
    #cv2.waitKey(0)

    _, contours, _ = cv2.findContours(mask, 1,2)

    # returns true if birds found 
    for cnt in contours:
        if cv2.contourArea(cnt) > 0:
            return 1

def showImg(a,b,img):
    cv2.imshow('img', img)
    cv2.waitKey(0)

def main():
    while 1:
        # check health
        if Health.percentage() <= 0.20:
            print(Health.percentage())
            print("Low on Health!\nStopping!!")
            return
        # initial count of inventory
        n_items_in_inventory = RS.inventory_counter()
        # stops if inv full
        if n_items_in_inventory >= 28:
            print("Inventory Full\nScript stopped!")
            # drop items here, then continue script
            RS.inventory_counter(showImg)

            return
        # pickpockets guard
        find_ham_guard()
        # loop to wait while confuse
        #RandTime.randTime(0,4,0,0,8,9)
        RandTime.randTime(0,0,1,0,0,9)
        if RS.inventory_counter() > n_items_in_inventory:
            continue
        else:
            while 1:
                if find_yellow_birds():
                    # waits for confuse to stop to loop
                    while find_yellow_birds():
                        pass
                else:
                    break


main()
