#!/usr/bin/python2
import autopy
import time
import os
from modules import RandTime
from modules import Mouse
cwd = os.getcwd()

def printMenu():
   print("Top-Left: Play Back\nTop-Right: Record\nBottom-Left: Play File\nBottom-Right:Quit program ")	
 
def record():
    sx, sy = autopy.screen.get_size()
    #takes away the unusable coords
    sx -= 1
    sy -= 1
    #divides the coords to get center of screen
    sx //=2
    sy //=2

    with open('mstats', 'wr') as f:
        print("Recording in 3 Secs!")
        #moves mouse position to center of screen
        autopy.mouse.move(sx,sy)
        time.sleep(3)
        os.system('clear')

        print("Recording")
        print('Top-left STOP')
        while True:
            x, y = autopy.mouse.get_pos()
            if x == 0 and y == 0:
                    print("Stop Rec")
                    break
            x = str(x)
            y = str(y)
            
            f.write('X '+x+' Y '+y+'\n')
            time.sleep(.01)


def readlines(f):
    if f =='':
        print("Reading {}".format("mstats file"))
        with open('mstats', 'r') as f:
            for line in f:
                f = line.find("X")+1
                s = line.find("Y")
                x =int( line[f:s])
                y = int(line[s+2:])

                #Mouse.moveTo(x,y)
                autopy.mouse.move(x,y)
                #autopy.mouse.smooth_move(x,y)
                time.sleep(.01)
    else:
        try:
            print("Reading {}".format(f))
            with open(f, 'r') as f:
                for line in f:
                    f = line.find("X")+1
                    s = line.find("Y")
                    x =int( line[f:s])
                    y = int(line[s+2:])

                    #Mouse.moveTo(x,y)
                    autopy.mouse.move(x,y)
                    #autopy.mouse.smooth_move(x,y)
                    #time.sleep(.0005)
                    RandTime.randTime(0,0,1,0,0,1)
        except:
            print("Not a valid file!")
            time.sleep(1.5)

                                
def rec_play():
    #1366,798
    sx, sy = autopy.screen.get_size()
    #print(sx,sy)
    os.system('clear')
    printMenu()
    while True:
        x, y = autopy.mouse.get_pos()
        #print(x,y)
        time.sleep(.5)
        
        #play: btm-left
        if x == 0 and y == (sy-1):
            print("Read back File")
            f = str(raw_input('> '))
            readlines(f)
            os.system('clear')
            print("Done")
            time.sleep(1)
            os.system('clear')
            printMenu()
                
        #records: top-right 
        if x == (sx-1) and y == 0:
            print("Rec")
            record()
            print("done")
            time.sleep(1)
            os.system('clear')
            printMenu() 
        #top-left
        if x == 0 and y == 0:
            print("Play")
            readlines('')
            print("done")
            time.sleep(1)
            os.system('clear')
            printMenu() 


        #stops program: btm-right
        if x == (sx-1) and y == (sy-1):
            os.system('clear')
            print("Quiting!")
            break

rec_play()

