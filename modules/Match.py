#Match.py
import cv2
import numpy as np
import os

def this(img_pat, img_temp):
    """pass img_pat as a cv2 image format, img_temp as a file
    Passed Function to do w/e after finding img_temp"""
    cwd  = os.getcwd()
    if cwd not in img_temp:
        img_temp = cwd+img_temp
    if '.png' not in img_temp:
        img_temp = cwd+img_temp+'.png'
    #print for DEBUG
    #print(img_temp)
    #img_temp
    img_temp = cv2.imread(img_temp,0)
    #save for DEBUG
    #cv2.imwrite('img_temp', img_temp)
    w, h = img_temp.shape[::-1]
    res = cv2.matchTemplate(img_pat,img_temp,cv2.TM_CCOEFF_NORMED)
    threshold = .8 #default is 8 
    loc = np.where( res >= threshold)
    
    return loc, w, h 

def images(img_pat, img_temp,x,y, func):
    w, h = img_temp.shape[::-1]
    try:
        res = cv2.matchTemplate(img_temp,img_pat,cv2.TM_CCOEFF_NORMED)

    except Exception as e:
        print("cannot match")
        print(e)
    threshold = .9 #default is 8 
    loc = np.where( res >= threshold)
    
    for pt in zip(*loc[::-1]):#goes through each found image
        func(img_pat, x, y, pt, w, h)
        return 0
    return 1

    #return loc to be iterable outisde the function
    #also sometimes width and height of image is needed
