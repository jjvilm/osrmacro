#!/usr/bin/python3
import os
import subprocess

def centering():

    display_x = subprocess.getoutput('xdotool getdisplaygeometry')
    display_x = display_x[:4]
    display_x = int(display_x)
    display_x //= 2

    pos = display_x - 383
    os.system('xdotool search old windowmove {0} 0'.format(pos))
    #os.system('xdotool search old windowmove 0 0')

    #move window
    os.system('xdotool search old windowsize --sync 767 564')

centering()


