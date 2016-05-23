import random
import os
import cv2
import numpy as np

from modules import Screenshot
from modules import  RS

rsx, rsy = RS.position()
def TakeScr():
    global rsx
    global rsy

    x1 = rsx + 13
    y1 = rsy + 60 
    x2 = rsx + 500
    y2 = rsy + 352


    play_window = Screenshot.shoot(x1,y1,x2,y2, 'hsv')
    #finds red shades
    lower_red = np.array([110,90,60])
    upper_red = np.array([130,230,255])

    mask = cv2.inRange(play_window, lower_red, upper_red)
    mask2 = cv2.inRange(play_window, lower_red, upper_red)
    #res = cv2.bitwise_and(play_window, play_window, mask=mask)
    #cv2.imshow('res', res)

    image, contours, hierarchy = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[4]
    x, y, w, h = cv2.boundingRect(cnt)
    w = w/2
    h = h/2
    x += w/2
    y += h/2
    # Draws rectangle around it
    img = cv2.rectangle(mask, (x,y), (x+w, y+h), (0,0,0), 2)
    #gen random coords within bound
    while True:
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        cv2.imshow('Image', img)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()

TakeScr()
