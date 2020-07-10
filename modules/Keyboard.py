#Keyboard.py
from random import triangular
from time import sleep
import pyautogui

def write(characters):
    """Types the passed characters with random pauses in between strokes"""
    for char in characters:
        # delay between key presses--key UP/DOWN
        #autopy.key.toggle(s, True)
        pyautogui.keyDown(char)
        sleep(triangular(.050,0.300))
        pyautogui.keyUp(char)
        # delay after key UP--next key

def press(button):
    if button == 'enter':
        pyautogui.keyDown('enter')
        sleep(triangular(.050,0.300))
        pyautogui.keyUp('enter')

    else:
        pyautogui.key.toggle(pyautogui.key.button, True)
        pyautogui.keyDown(button)
        sleep(triangular(.050,0.300))
        pyautogui.keyUp(button)
