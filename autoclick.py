import autopy
import time
import random
from modules import Mouse
from modules import RandTime
from modules import Screenshot
from modules import Match
from modules import RS


def keep_clicking():
    time.sleep(3)
    cx, cy  = autopy.mouse.get_pos()
    x1 = cx - 2
    y1 = cy - 2
    x2 = cx + 2
    y2 = cy + 2
    timer = 0
    while timer < 30:
        if count_logs('/home/jj/github/osrmacro/imgs/mapleLog.png') == 0:
            x = random.randint(x1,x2)
            y = random.randint(y1,y2)
            Mouse.moveClick(x,y,1)
            timer += 1
            RandTime.randTime(0,0,1,0,9,9)
            time.sleep(7)
        time.sleep(10)
        RandTime.randTime(0,0,1,0,9,9)

def count_logs(template_file):
    rs_bag = RS.get_bag('only')
    loc, w, h = Match.this(rs_bag, template_file)
    count = 0
    for pt in zip(*loc[::-1]):
        count +=1
        break
    return count
def clicker(item):
    time.sleep(3)
    cx, cy  = autopy.mouse.get_pos()
    x1 = cx - 3
    y1 = cy - 3
    x2 = cx + 3
    y2 = cy + 3
    timer = 0
    if item == 'stringer':
        while timer < 30:
            x = random.randint(x1,x2)
            y = random.randint(y1,y2)
            Mouse.moveClick(x,y,1)
            timer +=1
            time.sleep(33)
            RandTime.randTime(0,0,1,0,0,9)
    else:
        while timer < 375:
            x = random.randint(x1,x2)
            y = random.randint(y1,y2)
            Mouse.moveClick(x,y,1)
            timer +=1
def alching(clicks):
    time.sleep(4)
    cx, cy  = autopy.mouse.get_pos()
    x1 = cx - 2
    y1 = cy - 2
    x2 = cx + 2
    y2 = cy + 2
    for c in range(clicks):

        RandTime.randTime(0,0,0,0,0,1)

        autopy.mouse.toggle(True,1)
        RandTime.randTime(0,0,0,0,0,1)
        autopy.mouse.toggle(False,1)

        RandTime.randTime(0,0,0,0,9,9)

        autopy.mouse.toggle(True,1)
        RandTime.randTime(0,0,0,0,0,1)
        autopy.mouse.toggle(False,1)

        #randomly moves mouse
        x = random.randint(x1,x2)
        y = random.randint(y1,y2)
        Mouse.moveTo(x,y)

        RandTime.randTime(2,1,5,2,7,9)


def click_camelot(clicks):
    time.sleep(4)
    cx, cy  = autopy.mouse.get_pos()
    x1 = cx - 1
    y1 = cy - 1
    x2 = cx + 1
    y2 = cy + 1
    for c in range(clicks):
        x = random.randint(x1,x2)
        y = random.randint(y1,y2)

        RandTime.randTime(0,0,0,0,0,1)

        autopy.mouse.toggle(True,1)
        RandTime.randTime(0,0,0,0,0,2)
        autopy.mouse.toggle(False,1)

        if random.randint(0,4)==0:
            Mouse.moveTo(x,y)
        RandTime.randTime(0,0,3,0,3,5)
        if not RS.antiban('magic'):
            time.sleep(1.5)

#click_camelot(106)
#alching(31)


def splasher():
    time.sleep(3)
    print('starting')
    cx, cy = autopy.mouse.get_pos()
    print('grabbed position')
    x1 = cx - 5
    y1 = cy - 5
    x2 = cx + 5
    y2 = cy + 5
    while True:
        x = random.randint(x1, x2)
        y = random.randint(y1, y2)
        Mouse.moveClick(x,y,1)
        multiplier = random.randint(1,5)
        print("waiting for {}".format((60*multiplier)//60))
        time.sleep(60*multiplier)
        RandTime.randTime(0,0,0,0,0,9)





#keep_clicking()#for fletching
#clicker('stringer')#for stringer#for stringing
n = int(raw_input('Alchables??\n>>'))
alching(n)
#RS.logout()
#import os
#os.system('sudo shutdown now')
