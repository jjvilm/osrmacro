import cv2
import numpy as np
from modules import Match
from modules import RS
from modules import Mouse
from modules import RandTime

def click_item(item):
    bag, bagx,bagy = RS.get_bag("bag x y")
    loc, w, h = Match.this(bag, item)
    for pt in zip(*loc[::-1]):
        x1 = pt[0] + bagx
        y1 = pt[1] + bagy

        x2 = x1 + w - ((w/2)/2)
        y2 = y1 + h - ((h/2)/2)

        # Moving first point inwards 
        x1 += (w/2) / 2
        y1 += (h/2) / 2

        # Gen random coords within the bound
        x,y = Mouse.genCoords(x1,y1,x2,y2)
        Mouse.moveClick(x,y,1)
        #RandTime.randTime(0,5,0,0,5,0)
        break

def back2bank():
    Mouse.randMove(709,111,714,113,1)
    RandTime.randTime(3,0,0,3,9,9)
    Mouse.randMove(703,119,709,121,1)
    RandTime.randTime(4,0,0,4,9,9)
    Mouse.randMove(394,174,480,201,1)
    
    
def run():
    counter = 0
    skipL = True
    skipT = True
    while True: 
        if skipL:
            click_item('/home/jj/github/osrmacro/imgs/willowLogs.png')
            skipL = False
        else:
            click_item('/home/jj/github/osrmacro/imgs/tinderbox.png')
            skipL = True
        if counter == 27:
            print("All BURNED!")
            break

        if skipT:
            click_item('/home/jj/github/osrmacro/imgs/tinderbox.png')
            skipT = False
        else:
            click_item('/home/jj/github/osrmacro/imgs/willowLogs.png')
            skipT = True
        RandTime.randTime(2,0,0,2,9,9)
        counter += 1
        print(counter)
            

run()
