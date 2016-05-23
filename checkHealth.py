#!/usr/bin/python2
"""NOT DONE WITH IT YET!!
WHEN DONE IT SHOULD BE ABLE TO REACH HEALTH NUMBER"""
from modules import RS
from modules import Screenshot
from modules import Match
import cv2


def checkHealth():
    rsx, rsy = RS.position()
    HEART_POS = (542,65,568,91)
    x1 = rsx + HEART_POS[0]
    y1 = rsy + HEART_POS[1]
    x2 = rsx + HEART_POS[2]
    y2 = rsy + HEART_POS[3]

    heart = Screenshot.shoot(x1,y1, x2, y2)
    #cv2.imwrite('DEBUG.heart.png', heart)
    return health

loc, w, h = Match.this(checkHealth(), 'health.png')
for pt in zip(*loc[::-1])
    print("FOUND")

