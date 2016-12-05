import numpy as np
import cv2
from modules import Screenshot
from modules import Mouse
import time
import random
import Imgdb

class AutoFish(object):
    def __init__(self):
        # loads image DB
        self.idb = Imgdb.ImgDb()
        #self.findFishingIcon()
        #self.findBankIcon()
        self.findFishBubbles()
        #self.findCageOption()
        #self.main()

    def mini_map_mask(self,low,high, template=None):
        x1 = 571
        y1 = 29
        x2 = 710
        y2 = 180
        mini_map = Screenshot.shoot(x1,y1,x2,y2,'hsv')
        # applies mask
        mask = cv2.inRange(mini_map, low, high)
        return mask, x1, y1

    def findFishingIcon(self):
        #fish color
        low = np.array([93,119,84])
        high = np.array([121,255,255])
        mask, mm_x, mm_y = self.mini_map_mask(low, high)

        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            x += mm_x 
            y += mm_y
            x2 = x + w 
            y2 = y + h 
            Mouse.randMove(x,y,x2,y2,1)
            run= 0 
            time.sleep(1)
            return 0
        return 1

    def findFishBubbles(self):
        # water bubbles
        #low = np.array([103,81,0])
        #high = np.array([111,255,255])
        play_screen = Screenshot.shoot(6,59,510,355,'hsv')

        low = np.array([220,50,100])
        high = np.array([255,255,255])
        mask = cv2.inRange(play_screen, low, high)

        #cv2.imshow('img', mask)
        #cv2.waitKey(0)

        kernel = np.ones((5,5), np.uint8)
        dilation = cv2.dilate(mask, kernel, iterations = 1)

        #cv2.imshow('dilation', dilation)
        #cv2.waitKey(0)

        _, contours, _ = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in random.choice(contours):
            (x, y, w, h) = cv2.boundingRect(c)
            x += 6 
            y += 59
            x2 = x + w 
            y2 = y + h 
            Mouse.randMove(x,y,x2,y2,3)
            time.sleep(1)
            # no
            if self.findCageOption():
                Mouse.randMove(0,0,700,500, 1)
                continue
            else:
                return

    def findBankIcon(self):
        # bank colo
        low = np.array([26,160,176])
        high = np.array([27,244,228])
        mask, mm_x, mm_y = self.mini_map_mask(low, high)

        cv2.imshow('mask', mask)
        cv2.waitKey(0)

        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            x += 568 
            y += 36
            x2 = x + w 
            y2 = y + h 
            Mouse.randMove(x,y,x2,y2,1)
            run= 0 
            time.sleep(1)
            return

    def findCageOption(self):
        """Finds cage option in fishing guild when right clicked on fish bubbles"""
        x1 = 5
        y1 = 25
        x2 = 767
        y2 = 524
        rs_window = Screenshot.shoot(x1,y1,x2,y2)
        #cv2.imshow('img',rs_window)
        #cv2.waitKey(0)
        rsc = rs_window.copy()
        # gets only all the black and white
        ret,thresh1 = cv2.threshold(rsc,0,255,cv2.THRESH_BINARY)
        # inverst to only get black cloros as white
        ret,thresh1 = cv2.threshold(thresh1,0,255,cv2.THRESH_BINARY_INV)

        _, contours,h = cv2.findContours(thresh1,1,2)

        for cnt in contours:
            # looks for biggest square
            if cv2.contourArea(cnt) <= 1695.0:
                continue
            # checks contour sides
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            # draws only if its squared
            if len(approx)==4:
                print("square of {}".format(cv2.contourArea(cnt)))
                cv2.drawContours(rs_window,[cnt],0,(255,255,255),-1)
                # get geometry of approx
                # add rs coords
                x,y,w,h = cv2.boundingRect(cnt)

                #combines rs_window coords
                x += x1
                y += y1

                # scrshot of option menu on play window
                img = Screenshot.shoot(x,y,x+w,y+h)
                ret,thresh1 = cv2.threshold(img,254,255,cv2.THRESH_BINARY)

                # loads image from db
                img_from_dict = self.idb.pickled_dict['cage']


                #finds a match 
                from modules import Match
                # runs func when match is found returns true to keep looking for template
                if Match.images(thresh1,img_from_dict,x,y, self.doInMatched):
                    # keep looking for other bubbles
                    return 1
                else:
                    # found 'cage'
                    return 0
        # in case the options menu is aginast an edge
        return 1
                
    def doInMatched(self, *args, **kwargs):
        print("Found template")
        #unpacks args from Match.images
        img_pat,x,y,pt, w, h = args
        # combines pattern image w/ template coords
        x = pt[0]+x
        y = pt[1]+y
        # dimensions of pattern image
        img_pat_w, img_pat_h = img_pat.shape[::-1]
        # moves and clicks on the random passed coords
        Mouse.randMove(x,y,x+img_pat_w-10, y, 1)
        #cv2.rectangle(img_pat, pt, (pt[0] + w, pt[1] + h), (255,255,255), 2)

    def main(self):
        pass
       
af = AutoFish()

