#!/usr/bin/python2
#RS.py
import cv2
import numpy as np
import autopy
import subprocess
import os
import random
import time

#### My Modules 
import Screenshot
import Mouse
import RandTime
import Match





def position():
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
    return int(x), int(y)

def setWindowSize(w=767,h=564):
    geometry = subprocess.check_output(['xdotool','search','--name', 'Old','getwindowgeometry'])
    width = geometry[-7:-4]
    height = geometry[-3:]
    if width != w or  height != h:
        os.system('xdotool search --name Old windowsize --sync {0} {1}'.format(w,h))

    
def getOptionsMenu(x, y):#X,Y coords of where it right-clicked in bag to bring up the Options Menu
	"""Returns screenshot as menu, and menu_x, and menu_y which is topleft pt of the menu"""
	#Top-Left coords of where RS window is
	rs_x, rs_y = position()

	#Adding Rs coords to the options menu to get its location relevant to the window
	#24 here goes up on Y since sometimes screenshot needs to get more of the 
	#top Y to find the right option in the options menu.  
	menu_x = rs_x + x - 160  #higher number moves screenshot to left 
	menu_y = rs_y + y - 40  #moves screenshot up 

	menu_x2 = menu_x + 220 #Plus width
	menu_y2 = menu_y + 160 #Plus height 

	#takes screenshot here
	menu = Screenshot.shoot(menu_x, menu_y,menu_x2, menu_y2) 

	#added for debug purposes
        #cv2.imwrite('getOptionsMenu_debug.png', menu)

	#menu is the image, menuy/menux is the top-left coord of the image 
	return menu_x, menu_y, menu
    
#def findOptionClick(x,y,menu_x,menu_y, menu, option):#X,Y coords of where it clied in bag
def findOptionClick(x,y, option):#X,Y coords of where it clied in bag
    """Finds option based to the function from passed menu as cv2 image.  needs the x,y of the menu"""
    """DOES NOT RIGHT CLICK, MUST RIGHT CLICK TO USE THIS FUNCTION"""
    menu_x, menu_y, menu = getOptionsMenu(x,y)
    #get base directory osrmacro
    cwd = os.getcwd()
    if 'modules' in cwd: 
            occurance = cwd.rfind("/") #finds the last "/", returns its index
            cwd = cwd[:occurance+1] #'/home/user/osrmacro/'

    #added for debug purposes
    #cv2.imwrite('debug_FindOptionClick.png', menu)
    #cv2.imshow('Dbug_FindOptionClick',menu)

    #template
    template = cv2.imread(cwd+'/imgs/'+option+'.png',0)#0 here means turned gray

    w, h = template.shape[::-1]#Width, height of template image
    res = cv2.matchTemplate(menu,template,cv2.TM_CCOEFF_NORMED)
    threshold = .8 
    loc = np.where( res >= threshold)

    for pt in zip(*loc[::-1]):#goes through each found image
        pt_x, pt_y = pt #point of drop found inside the option menu screenshot
        #making btm coords
        btx = menu_x + pt_x + w
        bty = menu_y + pt_y + h
        #gen random coords
        pt_x = random.randint(menu_x+pt_x,btx)
        pt_y = random.randint(menu_y+pt_y,bty)

        #x = menu_x + pt_x + (random.randint(5,(w*2))) #generates random x range fr
        #y = menu_y + pt_y + (random.randint(5,h-1)) #generats random Y for drop selection
        
        Mouse.moveClick(pt_x,pt_y, 1)
        
        #autopy.mouse.click()#taking out since it does not delay the click
        RandTime.randTime(0,0,0,0,0,9)
        
def center_window():
    #display_x = subprocess.getoutput('xdotool getdisplaygeometry') python3 code
    display_x = subprocess.check_output(['xdotool','getdisplaygeometry'])
    display_x = display_x[:4]
    display_x = int(display_x)
    display_x //= 2

    pos = display_x - 383
    #moves window to center of screen
    os.system('xdotool search --name Old windowmove {0} 0'.format(pos))
    #os.system('xdotool search old windowmove 0 0')

def get_bag(bagornot):
    x1, y1 = position() #Get runescapes top-left coords

    x1 += 557    #make The Bag's top-left, and btm-right coords
	#y1=229 default for archlinux 
    y1 += 200    #x2,y2 == btm-right coord, width and height
    x2 = x1 + 173 
    y2 = y1 + 285#253default for arch
     
    rs_bag = Screenshot.shoot(x1,y1,x2,y2)
    #cv2.imwrite('rs_bag_debug.png',rs_bag)

    #returns image object, and top-left point of bag
    #returns image only if stringed passed
    if bagornot == 'only':
        return rs_bag
    else:
        return rs_bag, x1, y1

def getBankWindow():
    rsx, rsy = position() #Get runescapes top-left coords
    #creates bank window boundaries
    x1 = rsx + 21
    y1 = rsy + 23
    x2 = rsx + 486
    y2 = rsy + 335
    #gets screenshot object
    bankWindow = Screenshot.shoot(x1,y1,x2,y2)
    #save for debug
    #cv2.imwrite('debug_bankWindow.png', bankWindow)
    return bankWindow, x1, y1

def isBankOpen():
    """checks to see if bank is open, returns True, else False"""
    #get base directory osrmacro
    cwd = os.getcwd()
    if 'modules' in cwd: 
        occurance = cwd.rfind("/") #finds the last "/", returns its index
        cwd = cwd[:occurance+1] #'/home/user/osrmacro/'
    rsx,rsy = position()
    #position bank's close button, relative to RS window
    x1 = rsx+470
    y1 = rsy+10
    x2 = rsx+500
    y2 = rsy+55

    closeButton = Screenshot.shoot(x1,y1,x2,y2)
    #SAVE FOR DEBUG
    #cv2.imwrite('debug_closeButton.png',closeButton)
    loc, w, h = Match.this(closeButton, cwd+'/imgs/bankXbutton.png')
    #only runs if bank open
    for pt in zip(*loc[::-1]):
        return True
    return False

def closeBank():
    cwd = os.getcwd()
    rsx, rsy = position()
    x1 = rsx+470
    y1 = rsy+10
    x2 = rsx+500
    y2 = rsy+80

    closeButton = Screenshot.shoot(x1,y1,x2,y2)
    #SAVE FOR DEBUG
    #cv2.imwrite('debug_closeButton.png',closeButton)
    loc, w, h = Match.this(closeButton, cwd+'/imgs/bankXbutton.png')
    
    for pt in zip(*loc[::-1]):
        #making pt relative to the RS window
        pt = (pt[0] + x1, pt[1] + y1) 
        #make Btm-Right pt
        btx = pt[0] + w 
        bty = pt[1] + h 
        #gen random coords
        rx = random.randint(pt[0], btx)
        ry = random.randint(pt[1], bty)
        #Move to and Click the X to close bank
        Mouse.moveClick(rx,ry,1)
        break


def depositAll():
    rsx, rsy = position()

    x = rsx + random.randint(432,457)
    y = rsy + random.randint(320,348)

    Mouse.moveClick(x,y,1)
    RandTime.randTime(0,0,1,0,0,5)

def countItemInInv(template_file,*args):
    """Counts the N of items in INVENTORY
    if a number is passed it will count up to that"""
    #checks to see wheater to add cur dir or not
    if "/" not in template_file:
        template_file = os.getcwd()+"/imgs/"+template_file
    rs_bag = get_bag('only') #Screenshot taken here, 
    #saves image for DEBUG 
    #cv2.imwrite('debug_rs_bag_log_count.png',rs_bag)
    #loc == coordinates found in match
    loc, w, h = Match.this(rs_bag, template_file)
    #starts fount
    count = 0 
    for pt in zip(*loc[::-1]):#goes through each found image
        if args != ():
            if args[0] == 1:
                return 1
        count += 1
    #print(count)
    return count

def isInvEmpty():
    cwd = os.getcwd()
    bag = get_bag('only') 
    loc, w, h = Match.this(bag, cwd+'/imgs/emptySlot.png')
    
    for pt in zip(*loc[::-1]):
        #returns True if there is no itme in the first slot
        return True
    return False

def open_cw_bank():
    """Finds the visiblest square of the chest in castle wars bank, wors better when viewing from above at shortest distance."""
    
    # gets RS window's position
    rsx,rsy = position()
    # creates coords to take a screenshot of play window
    x1 = rsx + 13
    y1 = rsy + 60
    x2 = rsx + 500
    y2 = rsy + 352

    # Takes screenshot, as Hue-saturated-value image
    play_window = Screenshot.shoot(x1,y1,x2,y2, 'hsv')

    # Defines the hue to look for
    lower_gray = np.array([50,0,50])
    upper_gray = np.array([150,30,150])

    # Makes a black/white mask
    mask = cv2.inRange(play_window, lower_gray, upper_gray)
    res = cv2.bitwise_and(play_window, play_window, mask=mask)

    # Finds contours 
    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #collects the biggest contours
    possible_cnt = {}
    for cnt in contours:
        # Finds contours with 4 sides
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
        if len(approx)==4 and len(cnt) >4:
            possible_cnt[len(cnt)] = cnt

    # Will try to click in bank if all goes right
    try:
        biggest_cnt = max(possible_cnt.keys())

        #builds boundingrect 
        x,y,w,h = cv2.boundingRect(possible_cnt[biggest_cnt])
        
        #adds RS coords to the bounding box
        x += x1
        y += y1
        x2 = x + w
        y2 = y + h

        # generate random coords
        x = random.randint(x,x2)
        y = random.randint(y,y2)

        #move click chest
        Mouse.moveClick(x,y,1)
        time.sleep(1)
        
    except:
        print("Bank NOT found!\nMove camera around!")
    
def antiban(skill):
    if random.randint(0,10) == 0:
        rsx,rsy = position()
        # Tuples of locations
        #if random.randint(0,100) == 1:
        stats_btn = Mouse.genCoords(567,194,589,215)
        #                              x1  y1  x2  y2
        stats_window = Mouse.genCoords(557,234,729,470)
        
        #Clicks the skills button
        Mouse.moveClick(stats_btn[0]+rsx,stats_btn[1]+rsy,1)
        ## Randomly hovers over a random skill
        #Mouse.moveClick(stats_window[0]+rsx,stats_window[1]+rsy)

        #hovers over a certain skill
        skillHover(skill)
        #moves back to bag
        bagx,bagy = Mouse.genCoords(634,195,652,215)
        Mouse.moveClick(bagx+rsx,bagy+rsy,1)
        

def skillHover(skill):
    skills = {
            'attack':0, 'hitpoints':0,'mining':0,

            'strength':0,'agility':0,'smithing':0,

            'defence':0,'herblore':(620,295,662,311),'fishing':0,

            'ranged':0,'thieving':0,'cooking':0,

            'prayer':0,'crafting':0,'firemaking':0,

            'magic':0,'fletching':(620,389,666,406),'woodcutting':0,

            'runecraft':0,'slayer':0,'farming':0,
            
            'construction':0,'hunter':0
            }

    x1,y1,x2,y2 =skills[skill]
    x,y = Mouse.genCoords(x1,y1,x2,y2)
    Mouse.moveTo(x,y)
    RandTime.randTime(1,0,0,4,9,9)

def logout():
    rsx,rsy = position()
    #  Door Button
    x,y = Mouse.genCoords(636,495,650,515)
    x +=rsx
    y +=rsy
    Mouse.moveClick(x,y,1)

    # Log out Button
    x,y = Mouse.genCoords(581,428,707,450)
    x +=rsx
    y +=rsy
    Mouse.moveClick(x,y,1)

    
   




