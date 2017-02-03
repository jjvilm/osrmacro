import Screenshot
import cv2
import numpy as np
import pickle

class ImgDb(object):
    def __init__(self):
        self.pickled_file_path = '/home/jj/github/osrmacro/modules/itemdata.pickled'
        self.pickled_dict = {}

        #self.createImageDb()
        #self.savePickledDict()
        self.loadPickledDict()
        #self.showImgDb()

    def createImageDb(self):
        pass
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

    def scrnshtIntoDb(self,name,x1,y1,x2,y2):
        import time
        time.sleep(3)
        img4db = Screenshot.shoot(x1,y1,x2,y2)
        self.pickled_dict[name] = img4db
        print("Screenshot: '{}' added to dict".format(name))
        self.savePickledDict()

    def addImg(self,img_name,img):
        self.pickled_dict[img_name] = img
        print("Image: '{}' added to dict".format(img_name))
        self.savePickledDict()

    def rmImg(self,img_name=None):
        if img_name == None:
            img_name = raw_input("Name of image to remove:\n")
        del self.pickled_dict[img_name]
        print("\n{} removed from dict\n".format(img_name))
        self.savePickledDict()

    def savePickledDict(self):
        with open(self.pickled_file_path,'w') as f:
            pickle.dump(self.pickled_dict,f)
        print("saved dict as pickled in: {}\n".format(self.pickled_file_path))

    def loadPickledDict(self):
        with open(self.pickled_file_path,'r') as f:
            self.pickled_dict = pickle.load(f)
        #print("pickled dict loaded from: {}\n".format(self.pickled_file_path))

    def showImgDb(self):
        for key in self.pickled_dict.keys():
            try:
                print(key)
                img = self.pickled_dict[key]
                cv2.imshow('{}'.format(key),img)
                cv2.waitKey(600)
                cv2.destroyAllWindows()
            except Exception as e:
                print(e)
                continue

    def showImg(self,img_name):
        img = self.pickled_dict[img_name]
        cv2.imshow(img_name, img)
        cv2.waitKey(0)

    def listImgs(self):
        for i,key in enumerate(self.pickled_dict.keys()):
            print("{} {}".format(i,key))

    def turnBinary(self, img, *args):
        """Pass image as graysacle, else will be converted, other args include 'a' - add to DB, 'inv'-inverting, 's'-show"""
        #makes sure img is grayscale
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _,img = cv2.threshold(img, 254,255,cv2.THRESH_BINARY)
        print(img.shape)
        print("Turned Binary")
        try:
            for arg in args:
                # adds passed image to image db
                if arg == 'a':
                    img_name = raw_input("Name for image\n")
                    self.pickled_dict[img_name] = img
                    self.savePickledDict()
                # inverts binary img
                if arg == 'inv':
                    img_name = raw_input("Name for image\n")
                    _, img = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV)
                # shows img
                if arg == "s":
                    cv2.imshow('img',img)
                    cv2.waitKey(0)
        except:
            pass
        return img

    def append_parsed_dir(self,path):
        """pass full path to directory containing images"""
        import os
        for dirpath, dirname, filenames in os.walk(path):
            for cur_file in filenames:
                img = cv2.imread(dirpath+'/'+cur_file)
                # strips .png from file name
                cur_file_name = cur_file[:-4]
                self.addImg(cur_file_name, img)


if __name__ == "__main__":
    # loads image database
    imgdb = ImgDb()
    #imgdb.listImgs()
    #imgdb.showImg('drop')
    #imgdb.showImgDb()
    #imgdb.rmImg()
    #img = cv2.imread('/home/jj/tmp/pickpocket.png')
    img = imgdb.pickled_dict['drop']
    img = imgdb.turnBinary(img,'s','a')
    
    #imgdb.addImg('pickpocket',img)
