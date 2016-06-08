from modules import RS
from modules import Mouse
import time
import cv2
import numpy as np


# GET HSV img for mask and contours
img = cv2.imread('/home/jj/tmp/firealtar.png',1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def run():
    RS.press_button('equipment')
    tp_castle_wars()

def tp_dual_arena():
    # Teleports to Duel Arena
    x,y = Mouse.genCoords(689,395,712,417)
    Mouse.moveClick(x,y,3)
    RS.findOptionClick(x,y,'duelArenaTeleport')
def tp_castle_wars():
    x,y = Mouse.genCoords(689,395,712,417)
    Mouse.moveClick(x,y,3)
    RS.findOptionClick(x,y,'castleWarsTeleport')
def fire_altar():
    # lower and upper reddish colors for fire altar 
    low = np.array([0,65,31])
    high= np.array([18,99,146])

    # Mask
    mask = cv2.inRange(img, low, high)
    # Find Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[4]

    cv2.drawContours(img, [cnt], 0, (255,255,255), 3)
    cv2.imshow('img', mask)
    cv2.imshow('img2', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



#run()
fire_altar()
