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
def click(x,y,button=1, wait='no'):
    if wait == 'no':
        autopy.mouse.move(x,y)
        time.sleep(1)
        autopy.mouse.click(button)
    else:
        autopy.mouse.move(x,y)
        autopy.mouse.click(button)

def run():
    """To work keep directional needle pointing North"""
    ## Goes Outsides Desert Pines Storage
    map_click(486,592)
    time.sleep(9)
    ## Clicks the cave to go outside storage
    print("clicking outside")
    click(530,175)
    time.sleep(1)
    ## On map Clicks on Crystal Caves
    print("to CC")
    map_click(403,275)
    time.sleep(89)

    ## Clicks on CC to go inside
    print("Inside CC")
    click(500,275)
    #goes to sulphur
    map_click(392,41)
    mine()
    time.sleep(500)
    to_storage()

def mine():
    time.sleep(34)
    print("Mining the biggest sulphur rock")
    click(545,334)
def to_storage():
    map_click(727,130)
    time.sleep(34)
    click(545,245)
    time.sleep(1)
    map_click(430,491)
    time.sleep(83)
    click(466,303)
    map_click(486,522)
    time.sleep(8)
    click(513,328)
    time.sleep(1)
    # Stores all items
    click(401,81)
    # Closes Storage window and item window
    time.sleep(.5)
    click(407,26, 1,'no wait')
    click(813,28,1, 'no wait')



#setup()
run()
