#!/bin/python3
#from modules import RS as Rs
import time
import cv2
import numpy as np
from modules import Screenshot
from modules import Mouse
from pyclick import HumanClicker
from math import sqrt
from random import randint, random, triangular


#import autopy
class Enemy():
    def __init__(self):
        self.health = 0
        self.health_img = None
        self.mask = None
        # indicates weather enemy is targeted and being attacked
        self.targete = 0
        self.fight_length = 0

    def getHealth(self):
        # green color
        health_hsv = [ [69,22,134],[70,255,135] ]
        low = np.array(health_hsv[0])
        high = np.array(health_hsv[1])
        health_img = Screenshot.shoot(11,68,136,69,'hsv')
        self.health_img = health_img
        mask = cv2.inRange(health_img, low, high)
        self.mask = mask
        mask = [1 if x == 255 else x for x in mask[0]]
        #print(mask)
        self.health = int((sum(mask)/125) * 100)
        #self.health = sum(mask)
        print(f'Enemy HP:{self.health}%')

def main_run():
    # loop while waiting on emey to die
    def wait_loop():
        health_counter = 1
        enemy = Enemy()
        #waits until enemy health is 0
        start_time = time.time()
        while health_counter != 50:
            enemy.getHealth()
            cv2.imshow('health-hsv', enemy.health_img)
            cv2.imshow('mask', enemy.mask)
            cv2.waitKey(1)
            if enemy.health == 0:
                #time.sleep(random())
                print(f'Fight took:{time.time()-start_time:.2f} secs\nHealth Counter={health_counter}')
                health_counter = 1
                return
            health_counter += 1
            #time.sleep(1+random())


    # initialize HumanClicker object
    hc = HumanClicker()

    #dark_wizard = [ [27,70,22], [28,107,64] ]
    #hill giant
    dark_wizard = [ [20,46,34   ],[33,106,72 ] ]
    green_tile =  [ [61,113,105 ],[68,255,255] ]
    # low high hsv values
    player_tile = [ [87,232,190],[90,255,255] ]
    #gree_health_bar = [ [54,108,120],[62,255,255]]
    #red_health_bar = [ [0,254,254],[1,255,255] ]
    secs_wait = 1
    while 1:
        playScreen = Screenshot.shoot(0,0,520,360,'hsv')

        low = np.array(green_tile[0])
        high= np.array(green_tile[1])
        mask = cv2.inRange(playScreen,low,high)

        #kernel = np.ones((3,3), np.uint8)
        #closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        areas = {}
        # gathers areas with center coords
        for con in (contours):
            area =  cv2.contourArea(con)
            if area > 50:
                M = cv2.moments(con)
                #print(area)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                areas[area] = (cx,cy)
        # restarts loop if no emenies around
        if len(areas.keys()) == 0:
            print(f'No enemy detected...waiting {secs_wait} secs...')
            time.sleep(secs_wait)
            secs_wait += secs_wait * .20
            continue
        # find distance to 260,180 coords.  which is center of playing screen
        distances = {}
        for ele_set in areas.items():
            x = ele_set[1][0]
            y = ele_set[1][1]
            dist = int(sqrt(((260-x)**2) + ((180-y)**2)))
            distances[dist] = areas[ele_set[0]]
        # select point with min distance to center of play screen
        min_distance = min([i for i in distances.keys()])
        #print(f'minimum distance:{min_distance}')
        #print(f'coords:{distances[min_distance]}')

        # unpacks coords of tile closest to center of screen
        cx, cy = distances[min_distance]

        # move the mouse to position (100,100) on the screen in approximately 2 seconds
        hc.click(x=cx,y=cy)
        #autopy.mouse.move(cx,cy)
        #Mouse.moveTo(cx,cy)
        # wait after clicking to be able to see health box on top top of playscreen
        # time.sleep(2)
        # wait_loop()
        time.sleep(triangular(14,29)/1.5)
        # resets time to wait
        secs_wait = 1

main_run()
print('end')
