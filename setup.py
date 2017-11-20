#!/usr/bin/python3
import os
import subprocess

class window():
    def __init__(self):
        self.windowID = self.windowSelection()
        self.inOrigin()
        self.wind_stats()
        self.setDefaults()

    def windowSelection(self, window_n=None):
        print("Please select window to use")
        windowID = subprocess.getoutput('xdotool selectwindow')
        return windowID

    def wind_stats(self):
        #print(subprocess.getoutput('xdotool getwindowname {}'.format(self.windowID)))
        geometry = subprocess.getoutput('xdotool getwindowgeometry {}'.format(self.windowID))

        print(geometry)

    def setDefaults(self):
        geometry = (771, 539)
        goemetry_expanded = (1036, 539)
        os.system('xdotool windowsize {} {} {}'.format(self.windowID,geometry[0], geometry[1]))


    def centering(self):
        display_x = subprocess.getoutput('xdotool getdisplaygeometry')
        print(display_x)
        display_x = display_x[:4]
        display_x = int(display_x)
        display_x //= 2

        pos = display_x - 383
        #moves window to center of screen
        os.system('xdotool windowmove {} {} 0'.format(self.windowID,pos))
        #os.system('xdotool search old windowmove 0 0')


    def inOrigin(self):
        os.system('xdotool windowmove {} 0 0'.format(self.windowID))


if __name__ == '__main__':
    X = window()



