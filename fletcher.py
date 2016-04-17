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
cur_dir = os.getcwd()

def find_template(template_file, option=None):#pass template to function
#option == to option in menu when righ-clicked on item
    #checks to see wheater to add cur dir or not
    if "/" not in template_file:
        template_file = cur_dir+"/imgs/"+template_file
        
    rs_bag = RS.get_bag() #Screenshot taken here, 

    #loc == coordinates found in match
    loc, w, h = Match.this(rs_bag, template_file)
    for pt in zip(*loc[::-1]):#goes through each found image
        btmX = pt[0] + w - 5#pt == top-left coord of template, bottom-right point of of template image
        btmY = pt[1] + h - 5
        #moving the pt coord of the template a bit to the right, so options menu get brought up
        pt = (pt[0] + 5, pt[1] + 2)
        
        x, y = gen_coords(pt,btmX, btmY)#gets random x, y coords relative to RSposition on where to click
        if option == 'click':
            moveClick(x,y, 1)#left clicks on given x,y coords
        else:
            moveClick(x,y, 3)#right clicks on given x,y coords
            menu_x, menu_y, menu = RS.getOptionsMenu(x,y)#takes screenshot of options menu and returns the point at Top-left of the menu
            RandTime.randTime(0,0,0,0,0,1)
            
            RS.findOptionClick(x,y, menu_x, menu_y, menu, option)
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
	x1 = rsx + 21
	y1 = rsy + 23
	x2 = rsx + 486
	y2 = rsy + 335
	#creates  sceenshot object of bankwindow, 	
	bankWindow = Screenshot.shoot(x1,y1,x2,y2)

	#saves bankWindow image object for debug purposes
	#cv2.imwrite('bankWindow_debug.png',bankWindow)

	#loc == coordinates found in match
	loc, w, h = Match.this(bankWindow, template_file)
	for pt in zip(*loc[::-1]):#goes through each found image
		#adds x1,y1 coords to pt to be relative to the window
		pt = (x1+pt[0], y1+pt[1])

		#Bottom-Right coords of found template
		btmX =  pt[0] + w - 1
		btmY =  pt[1] + h - 1

		#create random coords within the coords of the found template
		rx = random.randint(pt[0],btmX)
		ry = random.randint(pt[1],btmY)

		#right clicks on given x,y coords
		print("RC @", rx,ry)
		Mouse.moveClick(rx,ry, 3)

		#takes screenshot & returns Top-left pt of screenshot
		menu_x, menu_y, menu = RS.getOptionsMenu(rx,ry)

		#saves image for debug purposes
		cv2.imwrite('debug_inBankLog.png',menu)

		RandTime.randTime(0,0,0,0,0,1)

		#following line does not work b/ option is set to click * 3 of width of option
		#only that is applicable for in bag inventory options
		#RS.findOptionClick(rx,ry, menu_x, menu_y, menu, option)

		#Using match instead to find option and click it
		print("cwd+'/imgs/'+option+'.png")
		loc, w, h = Match.this(menu, cwd+'/imgs/withdrawAll.png')

		
		#runs though the imgae to find 'withdraw all' option and click it
		for pt in zip(*loc[::-1]):
			pt = (menu_x+pt[0], menu_y+pt[1])

			#Bottom-Right coords of found template
			btmX =  pt[0] + w - 1
			btmY =  pt[1] + h - 1

			#create random coords within the coords of the found template
			rx = random.randint(pt[0],btmX)
			ry = random.randint(pt[1],btmY)

	XXXXX		#clicks on given random x,y coords
			print("RC @", rx,ry)
			Mouse.moveClick(rx,ry, 1)
			break
		
		break
	 
def gen_coords(pt,btmX,btmY):
    """Generates random coords of where to click once a template is found inside the bag screenshot"""
    x1 = pt[0] +( bag_coord[0][0] + 1) #gets top-left location of able to be right clicked
    y1 = pt[1] +( bag_coord[0][1] + 1)

    x2 = btmX +( bag_coord[0][0] -1) #bttm-right location able to be right clicked
    y2 = btmY +( bag_coord[0][1] -1)

    within_x = random.randint(x1,x2)#generates a range of clickable locations 
    within_y = random.randint(y1,y2)
    return within_x, within_y

def moveClick(x,y, button=1):#moves to random X,Y of found match of template
    """moves to x,y relative to the RS window"""
    rsx, rsy = RS.position()
    x = rsx + x
    y = rsy + y 
    Mouse.moveTo(x,y)

    autopy.mouse.toggle(True,button)
    RandTime.randTime(0,0,0,0,0,1)
    RandTime.randTime(0,0,0,0,0,0)
    autopy.mouse.toggle(False,button)
    
def moveToFletchingOptions():
    cwd = os.getcwd()
    rsx, rsy = RS.position() #gets position of RS window
    #x = rsx + random.randint(23,167)#x coord range of short bow
    #y = rsy + random.randint(397,469) #y respectivaly

    x = rsx + random.randint(209,299)#x coord range of long bow
    y = rsy + random.randint(395,456) #BR-coord of longbow

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

        RandTime.randTime(0,0,0,0,0,9)
        RandTime.randTime(0,0,0,0,0,0)

        #moves to 'Make X'
        Mouse.moveTo(x_a,y_a)

        RandTime.randTime(0,0,0,0,0,1)
        RandTime.randTime(0,0,0,0,0,0)
        #clicks on 'Make X'
        Mouse.click(1)

        time.sleep(.9)
        RandTime.randTime(0,0,0,0,9,9)

        Keyboard.type_this("99")
        autopy.key.toggle(autopy.key.K_RETURN, True)
        RandTime.randTime(0,0,0,0,0,1)
        RandTime.randTime(0,0,0,0,0,0)
        autopy.key.toggle(autopy.key.K_RETURN, False)
        break

def checkBank():
	rsx,rsy = RS.position()
	cwd= os.getcwd()
	#position of bank X button relative to rs.position
	x1= rsx+470
	y1= rsy+10
	x2= rsx+500
	y2= rsy+55
	timer = 1 
	while timer < 11:
		#fletch 
		find_template('knife.png','click')
		find_template('mapleLog.png','click')
		moveToFletchingOptions()
		#wait for flethcing to be done
		time.sleep(5)#50 for full inv
		#check for 5 seconds if bank is open, if not then done
		while timer < 11:
			print(timer)
			bankXButton = Screenshot.shoot(x1,y1,x2,y2)
			#cv2.imwrite('bankXbutton_debug.png', bankXButton)
			loc, w, h = Match.this(bankXButton,cwd+'/imgs/bankXbutton.png')
			#Only runs if bank is open
			for pt in zip(*loc[::-1]):
				#deposit long/short bows, take out logs
				find_template('mapleLongBow.png','depositAll')
				withdraw_from_bank('mapleLog.png','withdrawAll')
				checkBank()
				break
			time.sleep(1)
			timer += 1
    

if __name__ == '__main__':
    checkBank()
    #find_template('knife.png','click')
    #find_template('mapleLog.png','click')
    #moveToFletchingOptions()
    #print("Time taken:",timer)

