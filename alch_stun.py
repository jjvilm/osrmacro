#!/bin/python
import os
import random
import time
from subprocess import check_output
repeat = 10
alch = 0 # Here you can tufn off and on Alching or Stunning
stun = 0 # 1 is ON 0 is OFF

def itemLoc(item):
    items_ = {
    "book":"{0} {1}".format(random.randint(760,777), random.randint(268,296 )), 
    "alch":"{0} {1}".format(random.randint(741,749), random.randint(418,428 )),
    "bow":"{0} {1}".format(random.randint(725,744), random.randint(421,439 )),
    "stun":"{0} {1}".format(random.randint(643,654), random.randint(515,527 )),
    "wizard":"{0} {1}".format(random.randint(279,286), random.randint(310,320 ))
    }
    return items_[item]


def autoAlch():
    book = itemLoc("book")
    alch = itemLoc("alch")
    bow = itemLoc("bow")

    os.system("xdotool mousemove --sync {0}".format(book))
    os.system("xdotool click --delay {0} 1".format(random.randint(1511,2123)))
    randomTime()
    os.system("xdotool mousemove --sync {0}".format(alch))
    os.system("xdotool click --delay {0} 1".format(random.randint(1357,1787)))
    randomTime()
    os.system("xdotool mousemove --sync {0}".format(bow))
    os.system("xdotool click --delay {0} 1".format(random.randint(1435,2477)))
    randomTime()

def stunEnemy():
    stun = itemLoc("stun")
    wizard = itemLoc("wizard")
    book = itemLoc("book")

    os.system("xdotool mousemove --sync {0}".format(book))
    os.system("xdotool click --delay {0} 1".format(random.randint(1511,2123)))
    randomTime()		
    os.system("xdotool mousemove --sync {0}".format(stun))
    os.system("xdotool click --delay {0} 1".format(random.randint(1557,2477)))
    randomTime()
    os.system("xdotool mousemove --sync {0}".format(wizard))
    os.system("xdotool click --delay {0} 1".format(random.randint(1637,2377)))


def randomTime():
    fdigit = str(random.randint(1,2))
    sdigit = str(random.randint(1, 9))
    generatednumber = fdigit+"."+sdigit
    generatednumber = float(generatednumber)
    timeis = time.sleep(generatednumber)

def moveWindow(name, x=0, y=0):
    #"""Finds window ID based on given name of the window"""
    window_id = os.system("xdotool search --name {0}".format(name))
    #window_id = str(window_id)
   # window_id = window_id[2:-3]
   # if findWindowPos(window_id) == "10,129":
   #     return 0
   # else:
    os.system("xdotool windowmove {0} {1} {2}".format(window_id, x, y))


def findWindowPos(window):
    pos = check_output(["xdotool", "getwindowgeometry", "{0}".format(window)])
    pos = str(pos)
    first = pos.find(":")
    second = pos.find("(")
    pos = pos[first+1:second]
    return(pos)


def macro():
    findWindow("Old School Runescape")
    time.sleep(2)
    counter = 0
    os.system("clear")

    if alch == 0 and stun == 0:
        print("NOTHING TO DO!")
        return 0

    while counter <= repeat:
        if counter == repeat: 
            print('FINISHED!')
            break
        if alch == 1: 
            autoAlch()
        if stun == 1:
            stunEnemy()
        counter = counter+1
        os.system("clear")
        print(counter)


x = os.system("xdotool search --name old")
os.system("xdotool windowmove {0} 100 100".format(x))
