#Keyboard.py
import pyautogui
import time
import random

### My Modules
from modules import  RandTime
#from modules import RS

def type_this(strings):
    """Types the passed characters with random pauses in between strokes"""
    for s in strings:
        # delay between key presses--key UP/DOWN
        #autopy.key.toggle(s, True)
        pyautogui.keyDown(s)
        RandTime.randTime(0,0,0,0,0,5)
        pyautogui.keyUp(s)
        # delay after key UP--next key

def press(button):
    if button == 'enter':
        autopy.key.toggle(autopy.key.K_RETURN, True)
        RandTime.randTime(0,0,1,0,0,1)
        autopy.key.toggle(autopy.key.K_RETURN, False)

    else:
        autopy.key.toggle(autopy.key.button, True)
