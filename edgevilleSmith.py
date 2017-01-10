from modules import RS
from modules import Minimap
from modules import RandTime
import cv2
import numpy as np

furnance_hsv_values = ([11,135,91],[12,139,99])
# loop make sure bank is opened
while 1:
    # finds and clicks on bank booth window
    if RS.find_bank_booth():
        # loop waits till bank is open
        while 1:
            if RS.isBankOpen():
                break
            RandTime.randTime(0,0,0,0,9,9)
        # Close bank and loop
        RS.depositAll()
        RS.closeBank()
        break
    else:
        # Try to find Bank on Minimap
        Minimap.findBankIcon()


