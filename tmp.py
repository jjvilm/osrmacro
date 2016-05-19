import autopy
import os

import time

def start():
    autopy.mouse.move(6,27)
    autopy.mouse.click(1)
    time.sleep(1)
    autopy.key.toggle(autopy.key.K_LEFT, True)
    time.sleep(3)
    autopy.key.toggle(autopy.key.K_LEFT, False)

start()
