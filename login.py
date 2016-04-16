#!/usr/bin/python2
#login.py
import os
import random
import time
import subprocess
import autopy

### My modules
from modules import RS
from modules import Mouse
from modules import Keyboard 
from modules import RandTime

#geometry_w, geometry_h = (767,564)
#windowpid = 24540

#def rsPosition():
#    """Finds Old Runescape Window by name "old", returns the top-left coord as x,y
#	To make sure, the bag, and options menu coordinates are relevant to the window"""
#    rs_coords = subprocess.check_output(['xdotool','search','--name', 'Old','getwindowgeometry'])
#    rs_coords = str(rs_coords)
#    
#    ##Find the ":" and "," to get the coordinates after them 
#    first_occurance = rs_coords.find(":")#x, y coordinates extracted from window geometry
#    sec_occurance = rs_coords.find(",")
#    thr_occurance = rs_coords.find("(")
#    x = rs_coords[first_occurance+1: sec_occurance] #gets x coordinate
#    y = rs_coords[sec_occurance+1:thr_occurance] #gets y coordinate
#    
#    ##change from str to int
#    x = int(x) #x, y changed from str to int
#    y = int(y)
#    return x, y
    
#def findWindow(name): #find window name returns PID of the window
#    window = subprocess.getoutput('xdotool search --sync --name {0}'.format(name))#returns window's pid
#    return window
#
#def setWindowSize(window, x=767, y=564):#gets window geometry of Window (as a pid)
#    geometry = subprocess.getoutput('xdotool getwindowgeometry --pid {0}'.format(window))
#    width = geometry[-7:-4]
#    height = geometry[-3:]
#    if width != x and height != y:
#        os.system('xdotool windowsize --sync {0} {1} {2}'.format(window, x,y))
#        
        
            
def log_in_box(): #returns random coordinates for the login box
    x, y = RS.position()
    x = x + random.randint(277,492)
    y = y + random.randint(316,394)
    return x,y
                      
def log_in(user='no_user_given', passwd='nopass'):
    #sets default size if not already on default
    RS.setWindowSize()    
    rsx,rsy = RS.position()
    #moves to Existing User button
    Mouse.moveClick(rsx+(random.randint(403,530)),rsy+(random.randint(302,326)), 1)
    #Types user name
    Keyboard.type_this(user)
    #presses tab
    delay_mili = random.random()
    os.system('xdotool key --delay {0} Tab'.format(delay_mili))

    #Types password 
    Keyboard.type_this(passwd)
    #Moves to login button and clicks it
    Mouse.moveClick(rsx+(random.randint(238,365)),rsy+(random.randint(329,353)), 1)
    #Waits 4 secs after login in
    time.sleep(4)
    RandTime.randTime(0,0,0,0,0,9)
    #moves to login box(red login button)
    x, y = log_in_box()
    Mouse.moveClick(x,y)

def select_free_world():
    window = findWindow("Old")
    move_to_center()
    setWindowSize(window)

    time.sleep(1)

    os.system('xdotool mousemove --window {0} --sync {1} {2}'.format(window, 55,500)) #moves to 'world button' selectiion
    os.system('xdotool click 1')
    time.sleep(1)
    os.system('xdotool mousemove --window {0} --sync {1} {2}'.format(window, 520, 435))#moves to world 394 button
    time.sleep(1)
    os.system('xdotool click 1')
    time.sleep(2)


def logging():
    #select_free_world()
    log_in('', '')

if __name__ == '__main__':
    logging()
    
