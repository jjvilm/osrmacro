from modules import RS
from modules import Mouse
from modules import Screenshot
import time
import cv2
import numpy as np

# GET HSV img for mask and contours
#img = cv2.imread('/home/jj/tmp/firealtar.png',1)
# clones the img
#img_c = img.copy()
#img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def run():
    RS.press_button('equipment')
    tp_castle_wars()

def tp_duel_arena():
    RS.press_button('equipment')
    # Teleports to Duel Arena
    # moves to the ring equpiment
    x,y = Mouse.genCoords(689,395,712,417)
    Mouse.moveClick(x,y,3)
    RS.findOptionClick(x,y,'duelArenaTeleport')

def tp_castle_wars():
    RS.press_button('equipment')
    x,y = Mouse.genCoords(689,395,712,417)
    Mouse.moveClick(x,y,3)
    RS.findOptionClick(x,y,'castleWarsTeleport')

def detect_fire_altar():
    img = Screenshot.shoot(45,61,455,300, 'hsv')
    # lower and upper reddish colors for fire altar 
    low = np.array([0,74,107])
    high= np.array([13,110,137])

    # Mask
    mask = cv2.inRange(img, low, high)
    #cv2.imshow('mask', mask)

    try:
    ############################################################ Morphological closing
        """Using it to remove noise pixels inside the found object"""
        # kernel is the structuring element which decides the nature of operation
        kernel = np.ones((5,5), np.uint8)
        # closing is the img w/ no noise
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        #cv2.imshow('closing', closing)
    ################################################################ Gaussian blurr
        blur = cv2.GaussianBlur(closing, (5,5),0)
        #cv2.imshow('blur', blur)

    ################################################################# Contours
        # Find Contours
        """findContours fucntion modifies the source image.  so if you want to 
        source image even after finding contours, already store it to some other varialbe"""
        #                               source|cnt retrival mode |contour aprox method
        contours, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cnt = contours[1]

        #cv2.drawContours(img, contours, -1, (255,255,255), 1)
    ################################################################# Minimum enclosing circle
        #ellipse = cv2.fitEllipse(cnt)
        #cv2.ellipse(img_c, ellipse, (0,255,0),2)
    ################################################################# Rect around all contours

        all_xs = []
        all_ys = []
        # find max min x, y values of all contours
        for con in contours:
            for a in con:
                all_xs.append(a[0][0])
                all_ys.append(a[0][1])
        x1 = min(all_xs)
        y1 = min(all_ys)

        x2 = max(all_xs)
        y2 = max(all_ys)

        # Moving x in by half of half
        x1 += ((x2-x1)/2)/2
        x2 -= ((x2-x1)/2)/2
        # Moving Y in by half of half
        y1 += ((y2-y1)/2)/2
        y2 -= ((y2-y1)/2)/2
        # Adding Screenshot first point coords
        x1 += 45
        x2 += 45
        y1 += 61
        y2 += 61

        print(x1,y1,x2,y2)
        x, y = Mouse.genCoords(x1,y1,x2,y2)
        Mouse.moveClick(x,y,1)

        #print(x1,y1,x2,y2)
        # Drawing rect around the xs ys
        #cv2.rectangle(img, (x1,y1),(x2,y2),(255,255,255),1)

        #cv2.imshow('img', img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        return True
    except:
        print("Not found!\nTrying Again\n")
        time.sleep(.5)
        return False

def walk_to_fire_altar():    
    # detect green cactus, click on most northern one
    pass

tp_duel_arena()
time.sleep(9)
while not detect_fire_altar():
    pass
