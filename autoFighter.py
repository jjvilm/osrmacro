from modules import RS as Rs
from modules import Screenshot
import time
import cv2
import numpy as np

#for _ in xrange(1000):
#    Rs.antiban('magic')
#    time.sleep(1)
#
#dark_wizard = [ [27,70,22], [28,107,64] ]
# hill giant
dark_wizard = [ [13,13,50], [18,112,255]]
#gree_health_bar = [ [54,108,120],[62,255,255]]
#red_health_bar = [ [0,254,254],[1,255,255] ]

playScreen = Screenshot.shoot(7,27,520,360,'hsv')

low = np.array(dark_wizard[0])
high= np.array(dark_wizard[1])

mask = cv2.inRange(playScreen,low,high)
#cv2.imshow('img', mask)
#cv2.waitKey(0)

kernel = np.ones((3,3), np.uint8)

closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


_, contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

areas = {}

for i,con in enumerate(contours):
    area =  cv2.contourArea(con)
    if area > 1:
        Mouse.moveClick(
        print(area)
        areas[i] = area

#print(areas)
#cv2.imshow('img', mask)
#cv2.waitKey(0)
