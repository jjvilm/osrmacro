#Keyboard.py
import pyautogui
import time
from random import triangular

def write(strings):
    """Types the passed characters with random pauses in between strokes"""
    for s in strings:
        # delay between key presses--key UP/DOWN
        #autopy.key.toggle(s, True)
        pyautogui.keyDown(s)
        time.sleep(triangular(.050,0.300))
        pyautogui.keyUp(s)
        # delay after key UP--next key

def press(button):
    if button == 'enter':
        pyautogui.keyDown('enter')
        time.sleep(triangular(.050,0.300))
        pyautogui.keyUp('enter')

    else:
        pyautogui.key.toggle(pyautogui.key.button, True)
        pyautogui.keyDown(button)
        time.sleep(triangular(.050,0.300))
        pyautogui.keyUp(button)
