#!/bin/python3
# import sys
"""file to store all the hsv range values of all herbs"""

class Herb():
    def __init__(self):
        self.hsv_range = None
        self.herbdic = {
            "lantadyme":([78,225,50],[85,255,100]),
            "avantoe":([69,189,39],[73,213,106]),
            "irit":([46,0,52],[52,255,255]),
            "guam":([48,220,4],[65,255,83]),
            "grimmy":([18,181,29],[32,255,123]),
            "grimmy2":([20,228,9],[28,244,130])
               }
        # returns tuple of 2 lists, low high HSV range
        self.chooseHerbs()

    def chooseHerbs(self):
        """Displays available herbs, sets self.hsv_range to chosen herb"""
        # Prints the options
        for i, key in enumerate(self.herbdic.keys()):
            print(f"[{i}] : {key.upper()}")
        herbNo = 3
        # User input
        # Assure int input

        # while 1:
        #    # herbNo = input("\n***CHOOSE***\nHerb No.:")
        #    if herbNo.isalnum():
        #        herbNo = int(herbNo)
        #        break
        # Sets object's self.range value
        for i, key in enumerate(self.herbdic.keys()):
            if herbNo == i:
                self.hsv_range = self.herbdic[key]

if __name__ == '__main__':
    pass
