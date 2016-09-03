#!/usr/bin/python2
#stringer.py
from modules import RS
import os
from modules import Mouse
from modules import Match
from modules import RandTime
import random
#import autopy
import time
cwd = os.getcwd()
def checkInv(template):
    """Finds bowstring and unstrung bow in inventory and clicks them, if not found then returns false, true otherwise"""
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
    return False
        
def dobowstring(pt, w, h, bgx, bgy):
    rsx, rsy = RS.position()
    x, y = pt
    x +=   bgx 
    y +=  bgy   
    Mouse.moveClick(x,y, 1)

def makeBow():
    """selects option to "make all" bows when bowstring and unstrung bow are clicked"""
    rsx, rsy = RS.position()
    x = random.randint(rsx+220, rsx+300)
    y = random.randint(rsy+408, rsy+467)
    Mouse.moveClick(x,y, 3)

    #Remvoing RS coords 
    x -= rsx
    y -= rsy
    RS.findOptionClick(x,y,'makeAll')

def run():    
    RSX,RSY = RS.position()
    # Main stringer loop
    tries = 0 
    while True:
        if RS.isBankOpen():
            if tries == 2:
                print('Tries exausted, exiting!')
                #RS.logout()
                return 0
            #deposits all if inventory is not empty
            RS.depositAll()
            withdrawFromBank('/imgs/bowString.png')
            withdrawFromBank('/imgs/yewLongbowU.png')
            RS.closeBank()
            # starts stringing here 
            if checkInv(cwd+"/imgs/bowString.png") and checkInv(cwd+"/imgs/yewLongbowU.png"):
                makeBow()
                if RS.antiban('fletching'):
                    RandTime.randTime(11,0,0,11,9,9)
                else:
                    RandTime.randTime(15,0,0,15,9,9)
                #resets tries if items successfully found
                tries = 0
            else:
                RS.press_button('inventory')
                tries += 1
        else: 
         RS.open_cw_bank()
         RandTime.randTime(0,5,0,0,9,9)

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
#import os
#os.system('sudo shutdown now')
