"""This is a func part of RS module"""
import random
import os
import cv2
import numpy as np

from modules import Screenshot
from modules import  RS
from modules import Mouse

rsx, rsy = RS.position()
def castle_wars_bank():
    global rsx
    global rsy

    x1 = rsx + 13
    y1 = rsy + 60 
    x2 = rsx + 500
    y2 = rsy + 352


    play_window = Screenshot.shoot(x1,y1,x2,y2, 'hsv')
    #cv2.imwrite('bankchest.png',play_window)
    #play_window = cv2.imread('bankchest.png',-1)
    #finds red shades
    lower_red = np.array([50,0,50])
    upper_red = np.array([150,30,150])

    mask = cv2.inRange(play_window, lower_red, upper_red)
    #mask2 = cv2.inRange(play_window, lower_red, upper_red)
    res = cv2.bitwise_and(play_window, play_window, mask=mask)
    #cv2.imshow('res', res)

    # finds contours of image
    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # list to contain and get the max of all
    pos_cont = {}
    # Finds contours with edges higher than 4 that make a square
    for cnt in contours:
        # only gets the biegest contour
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        if len(approx)==4 and len(cnt) > 4:
            pos_cont[len(cnt)] = cnt
            print(len(cnt))
                
    try:
        biggest_cnt = max(pos_cont.keys())
        # builds a boundingrect
        x,y,w,h = cv2.boundingRect(pos_cont[biggest_cnt])
        # adds RS coords to these
        x += x1
        y += y1
        x2 = x + w
        y2 = y + h

        # gen.rand.coords
        x = random.randint(x,x2)
        y = random.randint(y,y2)

        Mouse.moveClick(x,y,1)
    except:
        print("Bank NOT found!")
    
castle_wars_bank()
