import autopy
import os
import time

def setup():
    os.system("xdotool search --name Eternal windowmove 0 0 ")

def map_click(x,y,button=1):
    """Move Click"""
    time.sleep(1)
    os.system('xdotool search --name Eternal windowactivate key Tab')
    time.sleep(.1)
    autopy.mouse.move(x,y)
    autopy.mouse.click(button)
    os.system('xdotool search --name Eternal windowactivate key Tab')
def click(x,y,button=1):
    autopy.mouse.move(x,y)
    time.sleep(2)
    autopy.mouse.click(button)


def run():
    """To work keep directional needle pointing North"""
    ## In Storage open map to go to sulphur mine
    map_click(486,592)
    time.sleep(10)
    ## Clicks the cave to go outside storage
    print("clicking outside")
    click(530,175)     
    time.sleep(2)
    ## On map Clicks on Crystal Caves
    print("to CC")
    map_click(403,275)
    
    time.sleep(89)

    ## Clicks on CC to go inside
    print("Inside CC")
    click(500,275)
    #goes to sulphur 
    map_click(392,41)

def mine():
    click(590,340)
def to_storage():
    map_click(727,130)
    
#setup()
#run()
to_storage()
