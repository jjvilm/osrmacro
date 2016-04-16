#!/usr/bin/python
import os
import random
import time
import subprocess

#geometry_w, geometry_h = (767,564)
#windowpid = 24540

def rsPosition():
    """Finds Old Runescape Window by name "old", returns the top-left coord as x,y
	To make sure, the bag, and options menu coordinates are relevant to the window"""
    rs_coords = subprocess.check_output(['xdotool','search','--name', 'Old','getwindowgeometry'])
    rs_coords = str(rs_coords)
    
    ##Find the ":" and "," to get the coordinates after them 
    first_occurance = rs_coords.find(":")#x, y coordinates extracted from window geometry
    sec_occurance = rs_coords.find(",")
    thr_occurance = rs_coords.find("(")
    x = rs_coords[first_occurance+1: sec_occurance] #gets x coordinate
    y = rs_coords[sec_occurance+1:thr_occurance] #gets y coordinate
    
    ##change from str to int
    x = int(x) #x, y changed from str to int
    y = int(y)
    return x, y
    
def findWindow(name): #find window name returns PID of the window
    window = subprocess.getoutput('xdotool search --sync --name {0}'.format(name))#returns window's pid
    return window

def setWindowSize(window, x=767, y=564):#gets window geometry of Window (as a pid)
    geometry = subprocess.getoutput('xdotool getwindowgeometry --pid {0}'.format(window))
    width = geometry[-7:-4]
    height = geometry[-3:]
    if width != x and height != y:
        os.system('xdotool windowsize --sync {0} {1} {2}'.format(window, x,y))
        
        
            
def log_in_box(): #returns random coordinates for the login box
    x = random.randint(277,492)
    y = random.randint(316,394)
    return x,y
                      
def log_in(user='no_user_given', passwd='nopass'):
	
	window = findWindow('Old')
	setWindowSize(window)

	x, y = log_in_box()
	WORK ON THIS LATER
	os.system('xdotool mousemove --window {0} --sync 456 310'.format(window))
	os.system('xdotool click 1')
	time.sleep(1)
	Keyboard.typing(user)
	
	
	os.system('xdotool key Tab')
	
	os.system('xdotool type --delay 50 {0}'.format(passwd))
	
	os.system('xdotool mousemove --window {0} --sync 298 336'.format(window))
	
	os.system('xdotool click 1')
	time.sleep(5)
	os.system('xdotool mousemove --window {0} --sync {1} {2}'.format(window, x, y)) #log in box coords
	time.sleep(1)
	os.system('xdotool click 1')

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

def move_to_center():
    display_x = subprocess.getoutput('xdotool getdisplaygeometry')
    display_x = display_x[:4]
    
    display_x = int(display_x)
    display_x //= 2
    
    
    
    pos = display_x - 383
    os.system('xdotool search old windowmove {0} 0'.format(pos))

def logging():
    select_free_world()
    log_in('', '')

logging()
    
