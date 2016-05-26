#!/usr/bin/python2
#stringer.py
from modules import RS
import os
from modules import Mouse
from modules import Match
import random
#import autopy
import time

cwd = os.getcwd()

def checkInv(template):
    rs_bag, bgx, bgy = RS.get_bag('bag and other variables')
    loc, w, h = Match.this(rs_bag,template )
    for pt in zip(*loc[::-1]):
        #assigns random values to pt 
        x, y = pt
        x = random.randint(pt[0], pt[0]+w)
        y = random.randint(pt[1], pt[1]+h)
        pt = (x,y)
        dobowstring(pt, w, h, bgx, bgy)
        return True
        
       
def dobowstring(pt, w, h, bgx, bgy):
    rsx, rsy = RS.position()
    x, y = pt
    x +=   bgx 
    y +=  bgy   
    Mouse.moveClick(x,y, 1)

def makeBow():
    rsx, rsy = RS.position()
    x = random.randint(rsx+220, rsx+300)
    y = random.randint(rsy+408, rsy+467)
    Mouse.moveClick(x,y, 3)

    #Remvoing RS coords 
    x -= rsx
    y -= rsy
    RS.findOptionClick(x,y,'makeAll')

def run():    
    RS.open_cw_bank()
    if RS.isBankOpen():
        #checks to see if inv is empty
        if not RS.isInvEmpty():
            #deposits all if inventory is not empty
            RS.depositAll()
        withdrawFromBank('/imgs/bowString.png')
        withdrawFromBank('/imgs/yewLongbowU.png')
        RS.closeBank()
    else: 
        if RS.isInvEmpty():
            return 0
        else:
            if RS.countItemInInv('bowString.png', 1)==1 and RS.countItemInInv('yewLongbowU.png',1)==1:
                pass
            else:
                return 0

    while True:
        if checkInv(cwd+"/imgs/bowString.png") and checkInv(cwd+"/imgs/yewLongbowU.png"):
            makeBow()
        time.sleep(17)
        while True:
            RS.open_cw_bank()
            if RS.isBankOpen():
                RS.depositAll()
                withdrawFromBank('/imgs/bowString.png')
                withdrawFromBank('/imgs/yewLongbowU.png')
                RS.closeBank()
                break

def withdrawFromBank(template_):
    rsx, rsy = RS.position()
    bankWindow, x1, y1 = RS.getBankWindow()
    loc, w, h = Match.this(bankWindow,template_)
    for pt in zip(*loc[::-1]):
        #unpackaged pt
        x, y = pt
        #make btm coords
        btmx = x + x1 + w - 5
        btmy = y + y1 + h - 5

        #add bankwindow+RS coords to pt
        x += x1 + 5
        y += y1 + 5
        #gen random coords
        x = random.randint(x,btmx)
        y = random.randint(y,btmy)

     
        Mouse.moveClick(x, y, 3 )
        #removing RS coords since they are added findOptionClick
        x -= rsx
        y -= rsy
        RS.findOptionClick(x,y,'withdraw14')
        break
run()
