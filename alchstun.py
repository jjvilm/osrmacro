import cv2
import numpy as np
from modules import Screenshot
from modules import  RS
import random
from modules import Mouse
from modules import RandTime

rsx, rsy = RS.position()
def findMonk():
    global rsx
    global rsy

    x1 = rsx + 13
    y1 = rsy + 60 
    x2 = rsx + 500
    y2 = rsy + 352

    play_window = Screenshot.shoot(x1,y1,x2,y2, 'hsv')
    #finds red shades
    lower_red = np.array([110,90,60])
    upper_red = np.array([130,230,255])

    #mask = cv2.inRange(play_window, lower_red, upper_red)
    mask2 = cv2.inRange(play_window, lower_red, upper_red)
    #res = cv2.bitwise_and(play_window, play_window, mask=mask)
    #cv2.imshow('res', res)

    image, contours, hierarchy = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0]

    x, y, w, h = cv2.boundingRect(cnt)
    w = w/2
    h = h/2
    x += w/2
    y += h/2
    # Draws rectangle around it
    #img = cv2.rectangle(mask, (x,y), (x+w, y+h), (0,0,0), 2)

    #makes x & y relative to RS window
    x += x1
    y += y1

    # returns half a square in the found contour
    return x,y,x+w, y+h

def genCoords(x1,y1,x2,y2):
    x = random.randint(x1,x2)
    y = random.randint(y1,y2)
    return x,y
def spell(*args, **kwargs):
    for s in args:
        if s == 'curse':
            x, y = genCoords(664+rsx,272+rsy,672+rsx,280+rsy)
            Mouse.moveClick(x,y, 1)
        elif s == 'alch':
            x, y = genCoords(710+rsx,346+rsy,720+rsx,356+rsy)
            Mouse.moveClick(x,y, 1)
            RandTime.randTime(0,1,0,0,1,9)
            x, y = genCoords(700+rsx,353+rsy,714+rsx,364+rsy)
            Mouse.moveClick(x,y, 1)
            RandTime.randTime(0,1,0,1,9,9)
        elif s == 'stun':
            x, y = genCoords(618+rsx,443+rsy,621+rsx,447+rsy)
            Mouse.moveClick(x,y,1)
        elif s == 'enfeeble':
            x, y = genCoords(686+rsx,416+rsy,696+rsx,426+rsy)
            Mouse.moveClick(x,y,1)

counter = 0
nats = int(raw_input("Alchabels??\n> "))
souls = int(raw_input("Souls??\n> "))
bodys = int(raw_input("Body runes??\n> "))
RS.press_button('magic')
while True:
    if counter >= nats+souls+bodys:
        print('done!')
        break
#        
    if nats:
        spell('alch')
        nats -= 1
        RandTime.randTime(0,1,9,0,3,9)
    if souls:
        spell('stun')
        souls -= 1
    if bodys and not souls:
        spell('curse')
        bodys -= 1
    if (counter % 10 == 0 or counter == 0) and ((souls > 0) or (bodys > 0)):
        print(counter,'Finding Monk')
        x1,y1,x2,y2 = findMonk()
    if (souls > 0) or (bodys > 0): 
        x, y = genCoords(x1,y1,x2, y2)
        Mouse.moveClick(x,y,1)
    counter += 1 
    RS.antiban('magic')
