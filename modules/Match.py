#Match.py
import cv2
import numpy as np
import os



def this(pattern_, template_):
    """pass pattern_ as a cv2 image format, template_ as a file
    Passed Function to do w/e after finding template"""
    cwd  = os.getcwd()
    if cwd not in template_:
        template_ = cwd+template_
    if '.png' not in template_:
        template_ = cwd+template_+'.png'
    #print for DEBUG
    #print(template_)
    #template
    template = cv2.imread(template_,0)
    #save for DEBUG
    #cv2.imwrite('debug_template_file', template_)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(pattern_,template,cv2.TM_CCOEFF_NORMED)
    threshold = .8 #default is 8 
    loc = np.where( res >= threshold)
    
    #following line NOT needed
    #for pt in zip(*loc[::-1]):#goes through each found image
    #    pass
    #return loc to be iterable outisde the function
    #also sometimes width and height of image is needed
    return loc, w, h 

#def thisAndDo(func):
#    cwd  = os.getcwd()
#    if cwd not in template_:
#        template_ = cwd+template_
#    if '.png' not in template_:
#        template_ = cwd+template_+'.png'
#    #print for DEBUG
#    #print(template_)
#    #template
#    template = cv2.imread(template_,0)
#    #save for DEBUG
#    cv2.imwrite('debug_template_file', template_)
#    w, h = template.shape[::-1]
#    res = cv2.matchTemplate(pattern_,template,cv2.TM_CCOEFF_NORMED)
#    threshold = .8 #default is 8 
#    loc = np.where( res >= threshold)
#    def wrapper_func(*args, **kwargs)
#        for pt in zip(*loc[::-1]):#goes through each found image
#
#    return loc, w, h 
if __name__ == "__main__":
    pass
