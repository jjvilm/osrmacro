import sys
"""file to store all the hsv range values of all herbs"""

def herb(name):
    name = name.lower()
    herbdic = {
        "lantadyme":([78,225,50],[85,255,100]),
        "avantoe":([69,189,39],[73,213,106]),
        "irit":([46,0,52],[52,255,255]),
        "guam":([48,220,4],[65,255,83]),
        "grimmy":([18,181,29],[32,255,123]),# used in bank to find thm
        "grimmy2":([20,228,9],[28,244,130]) #for use in inventory to find to clean
           }
    try:
        return herbdic[name]
    except Exception as e: # catch *all* exceptions
        #e = sys.exc_info()[0]
        #print( "Error: {}".format(e))
        print("Error in function herb .Herbdat",e)
        

