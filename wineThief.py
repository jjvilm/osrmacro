from modules import RS
from modules import RandTime
from modules import Mouse
import cv2
import numpy as np


def findWine():
    ######### find wine only in tabel!!! to make ti work better##########
    ps, psx, psy = RS.getPlayingScreen()

    lower = np.array([0,4,117])
    upper = np.array([16,22,182])

    mask = cv2.inRange(ps, lower, upper)

    _, contours, _  = cv2.findContours(mask.copy(), 1, 2)
    # find biggest area
    biggest_area = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > biggest_area:
            biggest_area = cv2.contourArea(cnt)

    # click on bnding rectangle of biggest area
    for cnt in contours:
        if cv2.contourArea(cnt) == biggest_area and biggest_area > 300:
            x,y,w,h = cv2.boundingRect(cnt)
            #cv2.rectangle(mask, (x,y), (x+w, y+h), (255,255,255), -1)
            x = x + psx
            y = y + psy

    #cv2.imshow('img', mask)
    #cv2.waitKey(0)
            Mouse.moveClick(x,y,1)
            return
##
def dropJug(x,y):
    Mouse.moveClick(x,y, 3)
    RS.findOptionClick(x,y,'drop')

def main():
    while 1:
        findWine()
        RandTime.randTime(1,0,0,1,9,9)

    # HSV range for wine in inventory
    #upper = np.array([0,100,74])
    #lower = np.array([26,255,224])

    #RS.inventory_counter(dropJug, upper, lower)
#findWine()
main()
#n = RS.inventory_counter()
#print(n)
