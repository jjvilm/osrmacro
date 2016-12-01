from modules import Screenshot
import cv2
import numpy as np
import pickle

class ImageStorage(object):
    def __init__(self):
        self.pickled_file_path = '/home/jj/github/osrmacro/modules/itemdata.pickled'
        self.pickled_dict = {}

        #self.createImageDb()
        #self.savePickledDict()
        self.loadPickledDict()
        self.showImgDb()

    def createImageDb(self):
        # shoots images at a predefined place
        pick = Screenshot.shoot(565,234,594,263)
        chisel = Screenshot.shoot(613,236,633,263)
        laws = Screenshot.shoot(649,242,678,263)
        souls = Screenshot.shoot(691,242,720,263)
        graceful_hood = Screenshot.shoot(573,273,591,296)
        graceful_cape = Screenshot.shoot(611,272,635,300)
        graceful_boots = Screenshot.shoot(651,274,677,296)
        graceful_top = Screenshot.shoot(692,274,720,297)
        graceful_legs = Screenshot.shoot(571,307,592,335)
        graceful_gloves = Screenshot.shoot(694,308,719,330)
        dramen_staff = Screenshot.shoot(609,307,633,336)
        ring_of_dueling = Screenshot.shoot(652,308,669,328)
        # dictonary of images
        self.pickled_dict['pickaxe'] = pick
        self.pickled_dict['chisel'] = chisel
        self.pickled_dict['laws'] = laws
        self.pickled_dict['souls'] = souls
        self.pickled_dict['graceful_hood'] = graceful_hood
        self.pickled_dict['graceful_cape'] = graceful_cape
        self.pickled_dict['graceful_boots'] = graceful_boots
        self.pickled_dict['graceful_top'] = graceful_top
        self.pickled_dict['graceful_legs'] = graceful_legs
        self.pickled_dict['graceful_gloves'] = graceful_gloves
        self.pickled_dict['dramen_staff'] = dramen_staff
        self.pickled_dict['ring_of_dueling'] = ring_of_dueling
        print("Shots taken! images stored to a dict\n")

    def savePickledDict(self):
        with open(self.pickled_file_path,'w') as f:
            pickle.dump(self.pickled_dict,f)
        print("saved dict as pickled in: {}\n".format(self.pickled_file_path))
    
    def loadPickledDict(self):
        with open(self.pickled_file_path,'r') as f:
            self.pickled_dict = pickle.load(f)
        print("pickled dict loaded from: {}\n".format(self.pickled_file_path))

    def showImgDb(self):
        for key in self.pickled_dict.keys():
            print(key)
            img = self.pickled_dict[key]
            cv2.imshow('{}'.format(key),img)
            cv2.waitKey(600)
            cv2.destroyAllWindows()

if __name__ == "__main__":
    img_dict = ImageStorage()
