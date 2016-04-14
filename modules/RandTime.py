import random
import time

def randTime(x,y,z,fdigit, sdigit, tdigit):#sleeps in  miliseconds from fdigit.sdigit+tdigit+random
    """x, y, z are the minimum millisecs"""
    #global timer
    
    random.seed()
    n = random.random()
    n = str(n)
    n = n[2:]
    
    fdigit = str(random.randint(x,fdigit))
    sdigit = str(random.randint(y,sdigit))
    tdigit = str(random.randint(z,tdigit))

    
    milisecs = fdigit+'.'+sdigit+tdigit+n
    milisecs = float(milisecs)
    #timer += milisecs
    time.sleep(milisecs)
