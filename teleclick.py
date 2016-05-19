import autopy
import time
import random

from modules import RandTime


def camelot():
    time.sleep(3)
    cx, cy = autopy.mouse.get_pos()

    x1 = cx - 1
    x2 = cx + 1
    y1 = cy -1 
    y2 = cy +1
    
    timer = 0

    while timer < 500:
        x = random.randint(x1,x2)
        y = random.randint(y1,y2)

        if random.randint(0,5) == 0:
            autopy.mouse.move(x,y)
            RandTime.randTime(0,0,0,0,0,1)
        print('clicking')
        autopy.mouse.toggle(True, 1)
        RandTime.randTime(0,0,0,0,0,1)
        autopy.mouse.toggle(False, 1) 

        RandTime.randTime(0,0,0,0,9,9)

        autopy.mouse.toggle(True, 1)
        RandTime.randTime(0,0,0,0,0,1)
        autopy.mouse.toggle(False, 1) 

        timer += 1
        time.sleep(2)
        RandTime.randTime(0,0,0,0,0,9)
       

camelot() 

