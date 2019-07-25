#!/usr/bin/python3
from modules import RandTime
import pyautogui
import random
import math
import time

"""Module to move mouse"""

mouseSpeed = 50

class MouseMovementCalculator:

    def __init__(self, gravity, wind, mouseSpeed, targetError):
        self.gravity = gravity
        self.wind = wind
        self.mouseSpeed = mouseSpeed
        self.targetError = targetError

    def calcCoordsAndDelay(self, startCoords, endCoords):
        veloX, veloY = (0, 0)
        coordsAndDelay = []
        xs, ys = startCoords
        xe, ye = endCoords
        totalDist = math.hypot(xs - xe, ys - ye)

        self._windX = 0
        self._windY = 0

        while True:
            veloX, veloY = self._calcVelocity(
                (xs, ys), (xe, ye), veloX, veloY, totalDist)
            xs += veloX
            ys += veloY

            w = round(
                max(random.randint(0, max(0, round(100 / self.mouseSpeed) - 1)) * 6, 5) * 0.9)

            coordsAndDelay.append((xs, ys, w))

            if math.hypot(xs - xe, ys - ye) < 1:
                break

        if round(xe) != round(xs) or round(ye) != round(ys):
            coordsAndDelay.append((round(xe), round(ye), 0))

        return coordsAndDelay

    def _calcVelocity(self, curCoords, endCoords, veloX, veloY, totalDist):
        xs, ys = curCoords
        xe, ye = endCoords
        dist = math.hypot(xs - xe, ys - ye)
        self.wind = max(min(self.wind, dist), 1)

        if dist == 0:
            return (veloX, veloY)

        maxStep = None
        D = max(min(round(round(totalDist) * 0.3) / 7, 25), 5)
        rCnc = random.randint(0, 5)
        #print(f"rCnc:{rCnc}")

        if rCnc == 1:
            D = 2

        if D <= round(dist):
            maxStep = D
        else:
            maxStep = round(dist)

        if dist >= self.targetError:
            self._windX = self._windX / \
                math.sqrt(3) + (random.randint(0, round(self.wind) * 2) -
                                self.wind) / math.sqrt(5)
            self._windY = self._windY / \
                math.sqrt(3) + (random.randint(0, round(self.wind) * 2) -
                                self.wind) / math.sqrt(5)
        else:
            self._windX = self._windX / math.sqrt(2)
            self._windY = self._windY / math.sqrt(2)

        veloX = veloX + self._windX
        veloY = veloY + self._windY
        veloX = veloX + self.gravity * (xe - xs) / dist
        veloY = veloY + self.gravity * (ye - ys) / dist

        if math.hypot(veloX, veloY) > maxStep:
            randomDist = maxStep / 2.0 + \
                random.randint(0, math.floor(round(maxStep) / 2))
            veloMag = math.sqrt(veloX * veloX + veloY * veloY)
            veloX = (veloX / veloMag) * randomDist
            veloY = (veloY / veloMag) * randomDist

        return (veloX, veloY)




def moveTo(x,y):
    startCoords = (pyautogui.position())
    endCoords = (x, y)
    # print(f"Moving to ({x},{y})")
    #                                      overshoot mousespeed  iterations
    # mouseCalc = MouseMovementCalculator(3, 3, -2, 2 * mouseSpeed)
    mouseCalc = MouseMovementCalculator(1, 3, mouseSpeed, 10 * mouseSpeed)
    coordsAndDelay = mouseCalc.calcCoordsAndDelay(startCoords, endCoords)

    pyautogui.moveTo(startCoords[0], startCoords[1])
    #time.sleep(3)
    #counting_iters = 0

    for x, y, delay in coordsAndDelay:
        #delay = delay / 10000
        #delay += random.random()
        #print(delay)
        pyautogui.moveTo(x, y)
        #time.sleep(delay)

        # counting_iters +=1
        # if counting_iters == 10:
        #     break


def click(btn):
    """Pass btn as 'left' or 'right'"""
    #autopy.mouse.click()
    #
    pyautogui.mouseDown(button=btn)
    RandTime.randTime(0,0,0,0,3,9)#time between click
    pyautogui.mouseUp(button=btn)


def moveClick(x,y, button):#moves to random X,Y of found match of template
    moveTo(x,y)
    # RandTime.randTime(0,0,0,0,0,2)
    #print(f"button passed {button}")
    if button == 1:
        pyautogui.mouseDown(button='left')
        RandTime.randTime(0,1,0,0,2,9)#time between click
        pyautogui.mouseUp(button='left')
    elif button == 3:
        pyautogui.mouseDown(button='right')
        RandTime.randTime(0,1,0,0,2,9)#time between click
        pyautogui.mouseUp(button='right')

def randCoord(pt,w,h ):
    """Takes a top-left point as pt, and width and height of template
        returns a pair of coordinates within the the size of the template, to be used with inventory bag items only"""
    w = pt[0]+w
    h = pt[1]+h
    # print(w)
    # print(h)

    x = random.randint(pt[0],w)
    y = random.randint(pt[1],h)
    return x,y

def genCoords(x1,y1,x2,y2):
    """Returns random coords of passed coordinates, not relative to RS window"""
    x = random.randint(x1,x2)
    y = random.randint(y1,y2)
    return x, y

def randMove(x1,y1,x2,y2,button):
    x, y = genCoords(x1,y1,x2,y2)
    if button == 1:
        moveClick(x,y,1)
    elif button == 3:
        moveClick(x,y,3)
    else:
        moveTo(x,y)

def mouse_loc():
    return pyautogui.position()

if __name__ == "__main__":
    print(mouse_loc())
