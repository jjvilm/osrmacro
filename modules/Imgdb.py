#from modules import Screenshot
#import Screenshot
import cv2
import numpy as np
import pickle
import pyautogui

class ImgDb(object):
    def __init__(self):
        self.pickled_file_path = '.\modules\itemdata.pickled'
        self.pickled_dict = {}
        self.loadPickledDict()

    def createImageDb(self):
        pass

    def scrnshtIntoDb(self,name,x1,y1,x2,y2):
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
        with open(self.pickled_file_path,'wb') as f:
            pickle.dump(self.pickled_dict,f)
        print("saved dict as pickled in: {}\n".format(self.pickled_file_path))

    def loadPickledDict(self):
        try:
            with open(self.pickled_file_path,'rb') as f:
                self.pickled_dict = pickle.load(f)
        except Exception as e:
            print(e)
            self.pickled_dict = {}



    def showImgDb(self):
        for key in self.pickled_dict.keys():
            try:
                print(key)
                img = self.pickled_dict[key]
                cv2.imshow('{}'.format(key),img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            except Exception as e:
                print(e)
                continue

    def showImg(self,img_name):
        img = self.pickled_dict[img_name]
        cv2.imshow(img_name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def listImgs(self):
        print("This ran")
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
    def promt_add(self):
        import os
        import pyautogui
        import time

        while 1:
            print(f"\n[1]Adding [2]show [0]Quit")
            item_name = input("Select action: ")
            os.system('clear')

            if item_name == '0':
                return
            elif item_name == '2':
                #display available items in dict
                for i, key in enumerate(self.pickled_dict.keys()):
                    print(f"[{i}]:{key}")

                print(f"Choose 0 - {len(self.pickled_dict)-1}")
                # select index from above
                item_name = input()
                #iterate and select appropriate
                for i, key in enumerate(self.pickled_dict.keys()):
                    if i == int(item_name):
                        self.showImg(key)
                continue
            elif item_name == '1':
                item_name = input("Item name:")
                print("move mouse to (x1,y1)")
                time.sleep(5)
                x1, y1 = pyautogui.position()
                print("move mouse to (x2,y2)")
                time.sleep(5)
                x2, y2 = pyautogui.position()
                self.scrnshtIntoDb(item_name,x1,y1,x2,y2)
                os.system('clear')
                self.showImg(item_name)
                continue


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
    itmImgDb = ImgDb()
    # itmImgDb.promt_add()

    # itmImgDb.listImgs()
    itmImgDb.showImgDb()
    #imgdb.rmImg()
    #img = cv2.imread('/home/jj/tmp/pickpocket.png')
    #img = imgdb.pickled_dict['drop']
    # imgdb.showImg('drop')
    #img = imgdb.turnBinary(img,'s','a')
    #imgdb.addImg('pickpocket',img)

    #interactive add
