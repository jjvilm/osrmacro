import autopy
import random
from modules import RandTime
from modules import Mouse

def readem(file_):
    rightclickstring = True
    clickstring = True
    rightclickbow = True
    clickbow = True
    closebank = True
    clickbow2 = True
    clickstring2 = True
    makebow = True
    

    with open(file_, 'r') as f:
        for line in f:
            f = line.find('X')+1
            s = line.find("Y")
            x = int(line[f:s])
            y = int(line[s+2:])
            
            #rightclicks string
            if x in range(942,963) and y in range(109,132) and rightclickstring == True:
                Mouse.click(3)
                rightclickstring = False
            #clicks string
            if x in range(854,1006) and y in range(185,198) and clickstring == True:
                print("In Range")
                Mouse.click(1)
                clickstring = False
            #right cliks bow
            if x in range(994,1017) and y in range(106,130) and rightclickbow == True:
                print("In Range")
                Mouse.click(3)
                rightclickbow = False
            #clicks bow 
            if x in range(854,1006) and y in range(185,198) and clickbow == True:
                print("In Range")
                Mouse.click(1)
                clickbow = False
            #closes bank
            if x in range(1057,1073) and y in range(36,62) and closebank == True:
                print("In Range")
                Mouse.click(1)
                closebank = False
            #clicks on string
            if x in range(1188,1207) and y in range(348,369) and clickstring2 == True:
                print("In Range")
                Mouse.click(1)
                clickstring2= False
            #clicks on bow
            if x in range(1234,1252) and y in range(348,369) and clickbow2 == True:
                print("In Range")
                Mouse.click(1)
                clickbow2 = False
            #right clicks make bow
            if x in range(790,940) and y in range(410,465) and makebow == True:
                print("In Range")
                Mouse.click(1)
                makebow = False
            ##clicks make all
            #if x in range(854,1006) and y in range(185,198) and clickbow == True:
            #    print("In Range")
            #    Mouse.click(1)
            #    clickbow = False

            autopy.mouse.move(x,y)
            RandTime.randTime(0,0,1,0,0,1)
readem('mstats')
