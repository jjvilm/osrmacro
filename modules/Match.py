import cv2
import numpy as np
import os



def this(pattern_, template_):
    """pass pattern_ as a cv2 image format, template_ as a file
    Passed Function to do w/e after finding template"""
    cur_dir = os.getcwd()
    print(cur_dir)
    #checks to see wheater to add cur dir or not
    if "/" not in template_:
        global cur_dir
        template_ = cur_dir+"/imgs/"+template_
        
    #template
    template = cv2.imread(template_,0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(pattern_,template_,cv2.TM_CCOEFF_NORMED)
    threshold = .8 #default is 8 
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):#goes through each found image
    #return loc to be iterable outisde the function
    return loc 
