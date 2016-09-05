import sys
"""file to store all the hsv range values of all herbs"""

def herb(name):
    herbdic = {
        "avantoe":([69,189,39],[73,213,106]),
        "irit":([46,135,77],[52,144,135]),
        "grimmy":([22,216,81],[26,236,119])

           }
    try:
        return herbdic[name]
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print( "Error: {}".format(e))
        

