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
    x1 = cx - 5
    y1 = cy - 5
    x2 = cx + 5
    y2 = cy + 5
    timer = 0
    while timer < 30:
        if count_logs('/home/jj/github/osrmacro/imgs/mapleLog.png') == 0:
            x = random.randint(x1,x2)
            y = random.randint(y1,y2)
            Mouse.moveClick(x,y,1)
            timer += 1
            time.sleep(9)
            RandTime.randTime(0,0,1,0,9,9)
        time.sleep(20)
        RandTime.randTime(0,0,1,0,9,9)

def count_logs(template_file):
    rs_bag = RS.get_bag()
    loc, w, h = Match.this(rs_bag, template_file)
    count = 0
    for pt in zip(*loc[::-1]):
        count +=1
        break
    return count
def clicker():
    time.sleep(3)
    cx, cy  = autopy.mouse.get_pos()
    x1 = cx - 5
    y1 = cy - 5
    x2 = cx + 5
    y2 = cy + 5
    timer = 0
    while timer < 30:
        x = random.randint(x1,x2)
        y = random.randint(y1,y2)
        Mouse.moveClick(x,y,1)
        timer +=1
        time.sleep(37)
        RandTime.randTime(0,0,1,0,0,9)

#keep_clicking()#for fletching
clicker()

