#!/usr/bin/python2
#fletcher.py
import cv2
import numpy as np
import autopy #for smooth mouse move
import pyscreenshot #to take screenshot of bag and options menu
import subprocess #needed to access xdotool output
import random #get random time
import time #for sleep
import os #needed to 

### Import my modules
from modules import Mouse
from modules import RandTime 
from modules import Screenshot
from modules import RS
from modules import Match
from modules import Keyboard
from modules import Screenshot

bag_coord =( ((557,200),(173,260)) )#runescape bag coords as x,y coord, w, h
cwd = os.getcwd()

def find_template(template_file, option=None):#pass template to function
    #option == to option in menu when righ-clicked on item
    #checks to see wheater to add cur dir or not
    if "/" not in template_file:
        template_file = cwd+"/imgs/"+template_file

    rs_bag, bagx,bagy = RS.get_bag("bag, and it's coords") #Screenshot taken here, 
    #loc is where the templates found are in 
    loc, w, h = Match.this(rs_bag, template_file)
    #for loops iterates through every found template
    for pt in zip(*loc[::-1]):#goes through each found image
        #pt = ((pt[0]+bagx),(pt[1]+bagy))
        #pt is the Top-left coord of the found template


        #create Bott-Right coord of found template
        btmX = pt[0] + w - 5 
        btmY = pt[1] + h - 5
        #moving the pt coord of the template a bit to the right, so options menu get brought up
        pt = (pt[0]+5, pt[1]+5)

        #gencoord adds RS position
        x, y = gen_coords(pt,btmX, btmY)#gets random x, y coords relative to RSposition on where to click
        #x, y = Mouse.randCoord(pt, w, h)
        if option == 'click' or option == 1:
            Mouse.moveClick(x,y, 1)#left clicks on given x,y coords
        else:
            Mouse.moveClick(x,y, 3)#right clicks on given x,y coords
            #menu_x, menu_y, menu = RS.getOptionsMenu(x,y)#takes screenshot of options menu and returns the point at Top-left of the menu
            RandTime.randTime(0,0,0,0,0,1)

            #RS.findOptionClick(x,y, menu_x, menu_y, menu, option)
            RS.findOptionClick(x,y,option)
        break
        
def withdraw_from_bank(template_file, option):#pass template to function
    #option == to option in menu options when righ-clicked on item
    #checks to see wheater to add cur dir or not
    cwd = os.getcwd()
    if "/" not in template_file:
            template_file = cwd+"/imgs/"+template_file
    #	print(template_file, "file in withraw_from_bank()")

    #creating bank window coords
    rsx,rsy = RS.position()
    #creates  sceenshot object of bankwindow, 	
    bankWindow, x1, y1 = RS.getBankWindow()
    #SAVE for DEBUG
    #cv2.imwrite('debug_inBankLog.png',bankWindow)
    
    #loc == coordinates found in match
    loc, w, h = Match.this(bankWindow, template_file)
    for pt in zip(*loc[::-1]):#goes through each found image
        #adds x1,y1 coords to pt to be relative to the window
        pt = (x1+pt[0]+5, y1+pt[1]+5)#
        #Bottom-Right coords of found template
        btmX =  pt[0] + w - 5
        btmY =  pt[1] + h - 5


        #create random coords within the coords of the found template
        rx = random.randint(pt[0],btmX)
        ry = random.randint(pt[1],btmY)

        if option == 'click':
            Mouse.moveClick(rx,ry,1)
        else:
            #right clicks on given x,y coords
            Mouse.moveClick(rx,ry, 3)
            RandTime.randTime(0,0,0,0,0,1)

            #Removing rsx,rsy coords from rx, ry 
            #becuase RS.getOptions adds them in by default
            rx -= rsx
            ry -= rsy

            RS.findOptionClick(rx,ry,'withdrawAll')
#            #takes screenshot & returns Top-left pt of screenshot
#            menu_x, menu_y, menu = RS.getOptionsMenu(rx,ry)
#
#            #saves image for debug purposes
#            #cv2.imwrite('debug_inBankLog_options.png',menu)
#
#            RandTime.randTime(0,0,0,0,0,1)
#            #Using match to find option and click it
#            loc, w, h = Match.this(menu, cwd+'/imgs/withdrawAll.png')
#
#            
#            #runs though the imgae to find 'withdraw all' option and click it
#            for pt in zip(*loc[::-1]):
#                #moves pt x to left *2 the w of it.  
#                pt = (menu_x+pt[0]-(w), menu_y+pt[1]+3)
#                
#
#                #Bottom-Right coords of found template
#                btmX =  pt[0] + w * 4
#                btmY =  pt[1] + h #mark
#
#                #create random coords within the coords of the found template
#                rx = random.randint(pt[0],btmX)
#                ry = random.randint(pt[1],btmY)
#
#                #clicks on given random x,y coords
#                Mouse.moveClick(rx,ry, 1)
#                break
	 
def gen_coords(pt,btmX,btmY):
    """Generates random coords of where to click once a template is found inside the bag screenshot"""
    x1 = pt[0] +( bag_coord[0][0] + 1) #gets top-left location of able to be right clicked
    y1 = pt[1] +( bag_coord[0][1] + 1)

    x2 = btmX +( bag_coord[0][0] -1) #bttm-right location able to be right clicked
    y2 = btmY +( bag_coord[0][1] -1)

    within_x = random.randint(x1,x2)#generates a range of clickable locations 
    within_y = random.randint(y1,y2)
    return within_x, within_y

    
def moveToFletchingOptions(bow):
    cwd = os.getcwd()
    rsx, rsy = RS.position() #gets position of RS window

    #x = rsx + random.randint(23,167)#x coord range of short bow
    #y = rsy + random.randint(397,469) #y respectivaly

    if 'magic' in bow:
        x,y = Mouse.genCoords(350,405,450,456)
    elif 'yew' in bow or 'maple' in bow:
        x = rsx + random.randint(215,280)#x coord range of long bow. Defautl 209,299
        y = rsy + random.randint(405,446) #BR-coord of longbow. Default: 395,456

    Mouse.moveClick(x,y,3) #right-clicks on short bow
    #taking away rs position since getoptionsmenu func adds them back in
    x = x - rsx
    y = y - rsy
    #gets screenshot
    menu_x, menu_y, menu = RS.getOptionsMenu(x,y)
    loc, w, h = Match.this(menu, cwd+'/imgs/makeX.png')
    #runs though the imgae to find it and click it
    for pt in zip(*loc[::-1]):
        pt_x, pt_y = pt #unpackes the pt into x,y

        x_a = menu_x + pt_x + (random.randint(1,(w*2)))
        y_a = menu_y + pt_y + (random.randint(5,h))

        RandTime.randTime(0,0,0,0,0,1)

        #moves to 'Make X'
        Mouse.moveTo(x_a,y_a)

        RandTime.randTime(0,0,0,0,0,1)
        #clicks on 'Make X'
        Mouse.click(1)

        time.sleep(1.1)
        RandTime.randTime(0,0,0,0,1,1)

        Keyboard.type_this("99")
        autopy.key.toggle(autopy.key.K_RETURN, True)
        RandTime.randTime(0,0,0,0,0,1)
        RandTime.randTime(0,0,0,0,0,0)
        autopy.key.toggle(autopy.key.K_RETURN, False)
        break

def start_fletching(bow):
    rsx,rsy = RS.position()
    cwd= os.getcwd()
    
    # Main Loop starts here
    while True:
        # Loop to withdraw knife and logs, and deposit and open bank
        while True:
            #runs only if bank is open
            if RS.isBankOpen():
    #   #   #   
                # try only 3 times to take out an item
                # otherwise starts stringing them
                tries = 0
    #   #   #
                # goes into loop to make sure a knife is taken out
                while True:
                    if tries == 3:
                        # Moves on to stringing if runs out of logs
                        return 0
                    # if inv is NOT empty deposit all items
                    if not RS.isInvEmpty():
                        RS.depositAll()

                    withdraw_from_bank('knife.png','click') 
                # goes into loop to make sure logs are taken out
                                        # works w/ yewLogs too
                    #withdraw_from_bank('mapleLog.png','withdrawAll') 
                    withdraw_from_bank(bow,'withdrawAll') 
                    RandTime.randTime(0,7,9,0,7,9)


                    if RS.countItemInInv('knife.png',1):
                        n_logs = RS.countItemInInv(bow)
                        if n_logs:
                            RS.closeBank()
                            break
                    tries += 1
    #   #   #
                #breaks out of the loop that makes sure items are deposited and withdrawn
                break
    #   #   #
                #Opens bank if it's not already opened
            else:
                RS.open_cw_bank()
                #gives time for bank detection to start
                RandTime.randTime(1,0,0,1,0,9)
    #   #   #  
        ########### Starts cutting logs ############
        # goes into a loop to make sure 
        # logs are being cut
        while True:
            #Finds knife, cliks it
            find_template('knife.png','click')
            RandTime.randTime(0,0,1,0,9,9)
    #   #   #
            #Finds First maple log, clicks it
            find_template(bow,'click')
    #   #   #
            #Moves to fletch short/long/stock
            #right cliks, make X, type 99
            moveToFletchingOptions(bow)
            RandTime.randTime(2,0,0,2,9,9)
    #   #   #
            if RS.countItemInInv('yewLongbowU.png',1):
                break
    #   #   # 
        #waits 2 secs/log 
        n_logs = (n_logs*2) - 7
        if RS.antiban('fletching'):
            n_logs -= 3
        RandTime.randTime(n_logs,0,0,n_logs,9,9)
    #   #   #

if __name__ == '__main__':
    start_fletching('magicLogs.png')
    os.system('./stringer.py')

