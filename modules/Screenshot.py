#!/usr/bin/python27
import cv2
import numpy as np
import pyscreenshot


def shoot(x1,y1,x2,y2, *args, **kwargs):
    """Takes screenshot at given coordinates as PIL image format, the converts to cv2 grayscale image format and returns it"""
    im = pyscreenshot.grab(bbox=(x1,y1,x2,y2)) #X1,Y1,X2,Y2
    #im.save('screenshot.png')
    #im=im.convert('RGB')
   
    im = np.array(im)
    

    cv_img = im.astype(np.uint8)
    try:
        if args[0] == 'hsv':
            hsv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
            return hsv_img
    except:
        pass
        
    
    cv_gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)

    #Saves image
    #cv2.imwrite('test1.png', cv_gray) ##to save img in cv2

    # Shows Image
    #cv2.imshow('Screenshot', cv_gray)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    return cv_gray



