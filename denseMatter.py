from modules import RS
from modules import Mouse
from modules import Screenshot
import Imgdb as imd 
import time
import cv2
import numpy as np

class CharacterActions(object):
    def __init__(self):
        self.rs_x, self.rs_y = RS.position() 

        self.telSalve()
        time.sleep(3)
        self.find_transportation_arrow()
        time.sleep(5)
        print('lookcing for fairly ring')
        self.find_fairy_ring()

    def check_list(self):
        items_dict = imd.ImageStorage()
        items_dict = items_dict.pickled_dict

        RS.press_button('equipment')
        time.sleep(1)
        for key in items_dict.keys():
            template = items_dict[key]
            #save for DEBUG
            #cv2.imwrite('debug_template_file', template_)
            w, h = template.shape[::-1]
            pattern = RS.get_bag('only','gray')
            res = cv2.matchTemplate(pattern,template,cv2.TM_CCOEFF_NORMED)
            threshold = .8 #default is 8 
            loc = np.where( res >= threshold)

            for pt in zip(*loc[::-1]):#goes through each found image
                print('{} found'.format(key))
                break
            else:
                print('{} not found'.format(key))

    def telSalve(self):
        RS.press_button('magic')
        Mouse.randMove(568,350,586,368,1)

    def find_transportation_arrow(self):
        run = 1
        # moves to north east area of mini map
        Mouse.randMove(680-20,65-20,680+20,65+20,1)
        time.sleep(5)
        while run:
            mini_map = Screenshot.shoot(571,29,718,180,'hsv')
            low = np.array([10,101,147])
            high = np.array([13,255,211])

            # applies mask
            mask = cv2.inRange(mini_map, low, high)
            # removes any noise
            kernel = np.ones((5,5), np.uint8)
            dilation = cv2.dilate(mask, kernel, iterations = 1)

            _, contours, _ = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for c in contours:
                (x, y, w, h) = cv2.boundingRect(c)
                x += 568
                y += 36
                x2 = x + w
                y2 = y + h 
                Mouse.randMove(x,y,x2,y2,1)
                run = 0
            time.sleep(1)
            print('running again')




        #cv2.imshow('img', dilation)
        #cv2.waitKey(0)
    def find_fairy_ring(self):
        run = 1
        while run:
            play_screen = Screenshot.shoot(6,59,510,355,'hsv')
            # finding white on fairy ring inner circle
            low = np.array([107,92,93])
            high = np.array([113,255,129])

            mask = cv2.inRange(play_screen, low, high)

            kernel = np.ones((10,10), np.uint8)
            dilation = cv2.dilate(mask, kernel, iterations = 1)
            #closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            #_,contours,_ = cv2,findContours(closing.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            _,contours,_ = cv2.findContours(dilation, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

            for con in contours:
                print("Area: {}".format(cv2.contourArea(con)))
                if cv2.contourArea(con) > 1.0:
                    (x, y, w, h) = cv2.boundingRect(con)
                    x += self.rs_x
                    y += self.rs_y
                    x1 = x
                    y1 = y
                    x2 = x + w
                    y2 = y + h
                    print("x1:{} y1:{} x2:{} y2:{}".format(x1,y1,x2,y2))
                    #print(cv2.contourArea(con))
                    #M = cv2.moments(con)
                    # finds centroid
                    #x,y = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    Mouse.randMove(x1,y1,x2,y2,3)
                    time.sleep(5)
                    if RS.findOptionClick(x1,y1,'cis'):
                        run = 0
                    time.sleep(2)
                    break

        #cv2.imshow('img', mask)
        #cv2.waitKey(000)

do = CharacterActions()
