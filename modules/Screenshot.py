#!/usr/bin/python27
import cv2
import numpy as np
import pyscreenshot


def shoot(x1,y1,x2,y2, *args, **kwargs):
    """Takes screenshot at given coordinates as PIL image format, the converts to cv2 grayscale image format and returns it"""
    # PIL format as RGB
    im = pyscreenshot.grab(bbox=(x1,y1,x2,y2)) #X1,Y1,X2,Y2
    #im.save('screenshot.png')

    # Converts to an array used for OpenCV
    im = np.array(im)
    # Next line needs to be taken out, messes up the array order when 
    # looking for hsv values
    #cv_img = im.astype(np.uint8)
    # Converts to BGR format for OpenCV
    cv_img = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    try:
        if args[0] == 'hsv':
            hsv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
            return hsv_img
    except:
        pass
        
    # have to convert from bgr to rgb first for next line 

    cv_gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    #Saves image
    #cv2.imwrite('test1.png', cv_gray) ##to save img in cv2

    # Shows Image
    #cv2.imshow('Screenshot', cv_gray)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    return cv_gray



