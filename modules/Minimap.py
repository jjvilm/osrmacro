import Screenshot
import Mouse
import cv2
import numpy as np
import RandTime

def get_mini_map_mask(low,high, template=None):
        # coords for the minimap
        x1 = 571
        y1 = 29
        x2 = 710
        y2 = 180
        mini_map = Screenshot.shoot(x1,y1,x2,y2,'hsv')
        # applies mask
        mask = cv2.inRange(mini_map, low, high)
        return mask, x1, y1

def findFishingIcon():
    #fish color
    low = np.array([93,119,84])
    high = np.array([121,255,255])
    mask, mm_x, mm_y = get_mini_map_mask(low, high)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        x += mm_x
        y += mm_y
        x2 = x + w
        y2 = y + h
        Mouse.randMove(x,y,x2,y2,1)
        run= 0
        RandTime.randTime(1,0,0,1,9,9)
        return 0
    return 1

def findBankIcon(*args):
    # bank hue range
    low = np.array([26,160,176])
    high = np.array([27,244,228])
    mask, mm_x, mm_y = get_mini_map_mask(low, high)

    #cv2.imshow('mask', mask)
    #cv2.waitKey(0)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        if args[0] == "n":
            x += 568
            y += 36
            x2 = x + w
            y2 = y + (h/2)

        x += 568
        y += 36
        x2 = x + w
        y2 = y + h
        Mouse.randMove(x,y,x2,y2,1)
        RandTime.randTime(1,0,0,1,9,9)
        return

if __name__ == "__main__":
    findBankIcon()
