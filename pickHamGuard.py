from modules import RS
from modules import Mouse
from modules import RandTime
import numpy as np
import cv2
import time

def find_ham_guard():
    try:
        ps, psx, psy = RS.getPlayingScreen()

        lower_pink = np.array([154,0,0])
        upper_pink = np.array([160,255,255])

        mask = cv2.inRange(ps, lower_pink, upper_pink)

        #cv2.imshow('img', mask)
        #cv2.waitKey(0)

        _, contours, _ = cv2.findContours(mask, 1,2)

        for cnt in contours:
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cx += psx
            cy += psy

            Mouse.moveClick(cx,cy, 3)
            break

        RS.findOptionClick(cx,cy, 'pickpocket')
    except Exception as e:
        print(e)

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

def main():
    while 1:
        n_items_in_inventory = RS.inventory_counter()
        if n_items_in_inventory >= 28:
            print("Inventory Full\nScript stopped!")
            return
        find_ham_guard()
        # loop to wait while confuse
        RandTime.randTime(1,5,0,1,9,9)
        if RS.inventory_counter() > n_items_in_inventory:
            continue
        else:
            while 1:
                if find_yellow_birds():
                    # waits for confuse to stop
                    while find_yellow_birds():
                        pass
                else:
                    break


main()
