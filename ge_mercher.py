from modules import Screenshot
from modules import setup
import pyautogui
import cv2
import time
import numpy as np
import random

class GE_Trading():

    def __init__(self):
        # below is tuple w/ 4 elements: x, y , w, h
        self.pos = 0
        
    def buy_slots(self):
        """ Returns available sell slot location by x, y, w, h """
        # gets trading window pos
        x, y, w, h = self.pos
        # find buy slots
        img = Screenshot.this(x, y, w, h, 'hsv')
        low = [32,248,192]
        high = [35,254,203]
        buy_slots = self.get_hsv_pattern_pos(img, low, high)

        buys = list()
        for cnt in buy_slots:
            rect = cv2.boundingRect(cnt)
            #pyautogui.moveTo(x, y)
            buys.append(rect)
        return buys #positions of buy arrow 

    def sell_slots(self):
        """ Returns available sell slot location by x, y, w, h """
        # gets trading window pos
        x, y, w, h = self.pos
        # find buy slots
        img = Screenshot.this(x, y, w, h, 'hsv')
        low = [16,248,122]
        high = [17,251,204]
        sells = self.get_hsv_pattern_pos(img, low, high)

        sell_slots = list()
        for cnt in sells:
            rect = cv2.boundingRect(cnt)
            #pyautogui.moveTo(x, y)
            sell_slots.append(rect)
        return sell_slots #positions of buy arrow 
            

    def get_hsv_pattern_pos(self, image=None,low_hsv=None,high_hsv=None):
        """Returns contours of location pattern is found"""
        low_hsv = np.array(low_hsv)
        high_hsv = np.array(high_hsv)
        mask = cv2.inRange(image, low_hsv, high_hsv)

        contours, h = cv2.findContours(mask, 1, 2)
        return contours



    def set_main_wndw(self):
        # gets screen size
        w, h = pyautogui.size()
        # takes screen screenshot. Returns  hsv format image
        scrn_scrnshot = Screenshot.this(0, 0, w, h, 'hsv')
        
        # find Grand exchange window
        # the  rectangule only the GE can have when GE Trading window active
        lower_hsv = np.array([12, 0, 7])
        upper_hsv = np.array([40, 62, 64])
        # mask of applied values
        mask = cv2.inRange(scrn_scrnshot, lower_hsv, upper_hsv)

        # find contours to get sides of rectangle
        contours, h = cv2.findContours(mask, 1, 2)

        for cnt in contours:
            # looks for biggest square
            # if cv2.contourArea(cnt) <= 1695.0:
            #    continue
            # checks contour sides
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

            # Squares are found with this code 
            # to find the rectangular GE window
            if len(approx) == 4:
                if cv2.contourArea(cnt) == 140123:
                    # position of GE Trading window found
                    x, y, w, h = cv2.boundingRect(cnt)
                    # add to take screenshot of GE trading window
                    w = x + w
                    h = y + h
                    self.pos = (x, y, w, h)
                    print(f"Trading window at:X={self.pos[0]} Y={self.pos[1]}")
                    return

    def add_randomness(self,level, *args, **kwargs):
        x = args[0] + self.pos[0]
        y = args[1] + self.pos[1]
        print(f"Before adding randomes X={x} Y={y}")
        nx = random.randrange(-level,level)
        ny = random.randrange(-level,level)
        x += nx
        y += ny
        print(f"After adding randomes X={nx} Y={ny}")
        return x,y

    def select(self, *args):
        #Setting for Buying
        if args[0] == 'buy':
            slots = self.buy_slots()
        #Setting for Selling
        elif args[0] == 'sell':
            slots = self.sell_slots()
        else:
            print("Make a selection buy or sell")

        ## picks random slot from buy/sell slots
        n = random.randint(0,len(slots) - 1)
        ## combines coords 
        pos = slots[n]
        x = pos[0]
        y = pos[1]
        ## adds randomness
        mx, my = self.add_randomness(17,x,y+15)
        pyautogui.moveTo(mx,my)
        time.sleep(.5)





    def main(self):
        self.select('sell')
        return

if __name__ == "__main__":
    Trade = GE_Trading()
    Trade.set_main_wndw()
    Trade.main()
