from modules import RS
from modules import Screenshot
from modules import Mouse

import random
import cv2 
import numpy as np
import time

RSX, RSY = RS.position()

def check_prayer():
    RSX, RSY = RS.position()
    pc = (545,109,571,135)
    prayer_level = Screenshot.shoot(pc[0],pc[1],pc[2],pc[3], 'hsv')
    
    low = np.array([116,0,0])
    high =np.array([141,255,255])

    mask = cv2.inRange(prayer_level, low, high)
    mask = np.array(mask)
     
    percentage = 0
    
    for color in mask:
        for element in color:
            if element == 255:
                percentage += 1
            else:
                continue
    return percentage/363.0

def find_prayer_pot():
    rs_bag, bagx, bagy = RS.get_bag('bag coords', 'hsv')
    # prayer potion color ranges
    low = np.array([78,140,0])
    high= np.array([81,225,211])
    mask = cv2.inRange(rs_bag, low, high)

    kernel = np.ones((5,5), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations = 1)
    
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for con in contours:
        x, y, w, h = cv2.boundingRect(con)
        cv2.rectangle(mask,(x,y), (x+w, y+h), (255,255,255),-1)

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for con in contours[::-1]:
        M = cv2.moments(con)
        mx, my = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        mx += RSX + bagx
        my += RSY + bagy

        mx += random.randint(-7,7)
        my += random.randint(-12,5)

        Mouse.moveClick(mx,my,1)
        #Mouse.moveTo(mx,my)
        break
        
def main():
    while True:
        p = check_prayer()
        print("{:.2f}".format(p))
        if p <= .50:
            find_prayer_pot()
            break
        time.sleep(3)

main()
