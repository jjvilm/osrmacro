from modules import RS
from modules import Mouse
import numpy as np
import cv2
import time


def find_ham_guard():
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


find_ham_guard()

