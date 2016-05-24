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

    with open('mstats', 'wr') as f:
        print("Recording in 3 Secs!")
        #moves mouse position to center of screen
        os.system('clear')

        print("Recording")
        print('Top-left STOP')
        ask = True
        while True:
            x, y = autopy.mouse.get_pos()
            if x != sx and y != sy:
                if x == 0 and y == 0:
                        print("Stop Rec")
                        break
                x = str(x)
                y = str(y)
                
                f.write('x '+x+' x '+y+'\n')
                time.sleep(.001)


def readlines(f):
    if f =='':
        print("Reading {}".format("mstats file"))
        with open('mstats', 'r') as f:
            for line in f:
                f = line.find("x")+1
                s = line.find("y")
                x =int( line[f:s])
                y = int(line[s+2:])

                #Mouse.moveTo(x,y)
                autopy.mouse.move(x,y)
                #autopy.mouse.smooth_move(x,y)
                time.sleep(.001)
    else:
        try:
            print("Reading {}".format(f))
            with open(f, 'r') as f:
                for line in f:
                    if 'r' in line:
                        continue
                    f = line.find("x")+1
                    s = line.find("y")
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
            os.system('clear')
            delete_loop(f)
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
def printMenu2():
    print("""top-left: Erase file\ntop-right: play again\nbtm-left: Read file\nbottom-right: exit file""")


def delete_loop(file_name):
    sx, sy = autopy.screen.get_size()
    os.system('clear')
    printMenu2()
    time.sleep(1)

    while True:
        x, y = autopy.mouse.get_pos()
        time.sleep(1)
        
        #top-left
        if x == 0 and y == 0:
            os.system('clear')
            print("Erasing")
            delete_file(file_name)
            print("done")
            time.sleep(1)
            os.system('clear')
            printMenu2()
        #records: top-right 
        if x == (sx-1) and y == 0:
            print("Play again")
            readlines(f)
            print("done")
            time.sleep(1)
            os.system('clear')
            printMenu2()
        #play: btm-left
        if x == 0 and y == (sy-1):
            print("Read back File")
            f = str(raw_input('> '))
            readlines(f)
            os.system('clear')
            print("Done")
            time.sleep(1)
            os.system('clear')
            printMenu2()

        #btm-right
        if x == (sx-1) and y == (sy-1):
            os.system('clear')
            print("Quiting!")
            break

def delete_file(file_name):
        with open(file_name, 'w') as f:
            f.write('')

rec_play()


