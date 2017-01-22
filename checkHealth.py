#!/usr/bin/python2
from modules import RS
from modules import Screenshot
import numpy as np
import cv2
import time


def checkHealth():
    rsx, rsy = RS.position()
    HEART_POS = (542,65,568,91)
    x1 = rsx + HEART_POS[0]
    y1 = rsy + HEART_POS[1]
    x2 = rsx + HEART_POS[2]
    y2 = rsy + HEART_POS[3]

    heart = Screenshot.shoot(x1,y1, x2, y2, 'hsv')

    lower = np.array([0,248,0])
    upper = np.array([4,252,255])
    mask = cv2.inRange(heart, lower, upper)
    # turns into array
    mask = np.array(mask)

    percentage = 0
    # counts pixels of value 255
    for color in mask:
        for element in color:
            if element == 255:
                percentage += 1
            else:
                continue

    #cv2.imwrite('DEBUG.heart.png', heart)
    #cv2.imshow('img',heart)
    #cv2.waitKey(0)
    print("{:.2f}".format(percentage/382.0))
    # 382 == full health
    return percentage/382.0

while 1:
    time.sleep(3)
    checkHealth()
