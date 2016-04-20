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
        break
        
       
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

    RS.findOptionClick(x,y,'makeAll')
def run():    
    if RS.isBankOpen():
        RS.depositAll()
        withdrawFromBank('/imgs/bowString.png')
        withdrawFromBank('/imgs/yewLongbowU.png')
        RS.closeBank()
    while True:
        checkInv(cwd+"/imgs/bowString.png")
        checkInv(cwd+"/imgs/yewLongbowU.png")
        makeBow()
        time.sleep(20)
        while True:
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
        x, y = pt
        x = rsx+x+x1
        y = rsy+y+y1
        Mouse.moveClick(x, y, 3 )
        RS.findOptionClick(x,y,'withdraw14')
        break
run()
