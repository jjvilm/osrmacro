import cv2
import numpy as np
import os



def this(pattern_a, template_b):
    """pass pattern_ as a cv2 image format, template_ as a file
    Passed Function to do w/e after finding template"""
    #cur_dir = os.getcwd()
    #checks to see wheater to add cur dir or not
    #if "/" not in template_b:
    #    template_b = cur_dir+"/imgs/"+template_b
    #    print("cwd in modules:",cur_dir)
    #print(template_b)
        
    #template
    template = cv2.imread(template_b,0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(pattern_a,template,cv2.TM_CCOEFF_NORMED)
    threshold = .8 #default is 8 
    loc = np.where( res >= threshold)
    
    #following line NOT needed
    #for pt in zip(*loc[::-1]):#goes through each found image
    #    pass
    #return loc to be iterable outisde the function
    #also sometimes width and height of image is needed
    return loc, w, h 
