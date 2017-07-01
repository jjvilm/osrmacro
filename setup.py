#!/usr/bin/python3
import os
import subprocess

windowName = 'RuneScape'

def centering():

    display_x = subprocess.getoutput('xdotool getdisplaygeometry')
    print(display_x)
    display_x = display_x[:4]
    display_x = int(display_x)
    display_x //= 2

    pos = display_x - 383
    #moves window to center of screen
    os.system('xdotool search {} windowmove {0} 0'.format(windowName,pos))
    #os.system('xdotool search old windowmove 0 0')


def move2origin():
    os.system('xdotool search {} windowmove 0 0'.format(windowName))


#centering()
move2origin()
os.system('xdotool search --name {} windowsize 767 564'.format(windowName))


