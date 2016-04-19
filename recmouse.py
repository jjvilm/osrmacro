import autopy
import time
import os
from modules import RandTime
from modules import Mouse
cwd = os.getcwd()

def record():
    sx, sy = autopy.screen.get_size()
    sx -= 1
    sy -= 1
    sx //=2
    sy //=2

    with open('mstats', 'wr') as f:
        print("Recording in 3 Secs!")
        autopy.mouse.move(sx,sy)
        time.sleep(3)
        os.system('clear')
        print("Recording")
        while True:
            x, y = autopy.mouse.get_pos()
            if x == 0 and y == 0:
                    print("Stop Rec")
                    break
            x = str(x)
            y = str(y)
            
            f.write('X '+x+' Y '+y+'\n')
            #time.sleep(.0005)
            RandTime.randTime(0,0,1,0,0,1)

def readlines(f):
    if f == None:
        with open('mstats', 'r') as f:
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
    else:
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

                                
def rec_play():
    #1366,798
    sx, sy = autopy.screen.get_size()
    #print(sx,sy)
    os.system('clear')
    print("Top-Left: Playback File\nTop-Right: Record\nBottom-Left: Play Back red\nBottom-Right:Quit program ")	
    while True:
        x, y = autopy.mouse.get_pos()
        #print(x,y)
        time.sleep(.5)
        
        #play: btm-left
        if x == 0 and y == (sy-1):
            print("Play")
            readlines(None)
            print("done")
            time.sleep(1)
            os.system('clear')
            print("Top-Left: Playback File\nTop-Right: Record\nBottom-Left: Play Back red\nBottom-Right:Quit program ")	
                
        #records: top-right 
        if x == (sx-1) and y == 0:
            print("Rec")
            record()
            print("done")
            time.sleep(1)
            os.system('clear')
            
            print("Top-Left: Playback File\nTop-Right: Record\nBottom-Left: Play Back red\nBottom-Right:Quit program ")	
        #top-left
        if x == 0 and y == 0:
            print("Read back File")
            f = input('> ')
            readlines(f)
            os.system('clear')
            print("Done")
            time.sleep(1)
            os.system('clear')
            print("Top-Left: Playback File\nTop-Right: Record\nBottom-Left: Play Back red\nBottom-Right:Quit program ")	


        #stops program: btm-right
        if x == (sx-1) and y == (sy-1):
            print("Quiting!")
            break

rec_play()

