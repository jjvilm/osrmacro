from modules import RS
from modules import Minimap
from modules import RandTime
import cv2
import numpy as np

furnance_hsv_values = ([11,135,91],[12,139,99])

# finds and clicks on bank booth window
if RS.find_bank_booth():
    # waits till bank is open
    while 1:
        if RS.isBankOpen():
            break
        RandTime.randTime(0,0,0,0,9,9)
    RS.depositAll()
else:
    Minimap.findBankIcon()


