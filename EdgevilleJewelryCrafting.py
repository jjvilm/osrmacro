#!/bin/python3
import functools
import cv2
import numpy as np
from modules import Screenshot, osr
from random import triangular
from time import sleep,time
from datetime import datetime


def decorator(func):
    """ used to allow a passable variable to object's methods,
    to terminate program """
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        if args[1]:
            return
        else:
            func(*args, **kwargs)
        # Do something after
        return
    return wrapper_decorator
class Craft():
    def __init__(self,jewel):
        self.Game = osr.Frame()
        self.jewel = jewel
        self.jewelry_type = 1 #1 ring,2 bracelt
        self.bank = True
        self.path_len = 10
        self.energy_recovery_time = time()
        self.run_energy = True
        self.terminate = 0
    def getJewelInfo(self,*args):
        """ returns hsv values of items passed to find in bank"""
        print(args)
        rsx = self.Game.rsx
        rsy = self.Game.rsy
        # set([[<low hsv>],[high hsv]],((<ring loc>),(<bracelet loc>)) )
        jewels = {  'diamond':([[0,4,168],[1,6,169]],#hsv
                        (rsx + 270, rsy + 190)),#coords
                    'ruby':([[0,227,79], [4,245,99]],
                        (rsx + 220, rsy + 192)),
                    'emerald':([[56,202,188],[57,223,189]],
                        (rsx + 160, rsy + 130),#emerald ring coords
                        (rsx + 170, rsy + 310)),#bracelet
                    'topaz':([[162,223,80],[169,233,180]],
                        (rsx + 227, rsy + 219)),#ammy
                    'necklace':([[0,204,0],[26,235,255]]),
                    'silver':([[118,17,76],[120,21,185]]),
                    'gold':([[23,224,177],[24,226,220]],
                        (rsx + 77, rsy + 127)) # gold rings coords
                        }
        return jewels[args[0]]
    @decorator
    def backForth(self,*args):
        def get_markedtile_coords(pnt):
            x,y = pnt
            #self.Game.hc.move((x,y),duration=self.rinterval('duration'))
            self.Game.hc.click(x=x,y=y)
            #print(f"{x,y}")
            return

        if self.Game.isRunActive():
            self.path_len = 5
            self.run_energy = True
            # print(f"Run is ACTIVE, length={self.path_len} secs")
        else:
            self.path_len = 10
            self.run_energy = False
            # print(f"Run is NOT ACTIVE, length={self.path_len} secs")


        while not self.terminate:
            game_scrn, sx, sy = self.Game.getPlayingScreen('hsv')
            # original yellow #FFFF00
            marked_tile = [[28,207,173],[37,255,255]]
            low = np.array(marked_tile[0])
            high= np.array(marked_tile[1])
            mask = cv2.inRange(game_scrn,low,high)
            # cv2.imshow('mask',mask)
            # cv2.waitKey(1)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # _ == None then check bank, go from there
            if type(_) == None:
                if self.Game.isBankOpen():
                    print("Bank was already open")
                    self.bank = False
                    return
            # get smaller values in x to keep bank on left
            bankFurnance_coords = {}
            for cnt in contours:
                # makes sure nothing too small is clicked
                if cv2.contourArea(cnt) < 30:
                    #print(cv2.contourArea(cnt))
                    continue

                try:
                    M = cv2.moments(cnt)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    rx = int(triangular(-5,5))
                    ry = int(triangular(-5,5))
                    x = cx+rx+sx
                    y = cy+ry+sy
                    bankFurnance_coords[(x,y)] = M
                except Exception as e:
                    print(e)
                    continue
            # clicks on marked bank tile
            if self.bank:
                # switch ensures bank is clicked b4 iter loop
                self.bank = False
                # print(f'self.bank = {self.bank}')
                # Do if bank open
                print("Found bank booth")
                try: # if bank is open then return
                    minx = min([pnt[0] for pnt in bankFurnance_coords.keys()])
                    pnt = [pnt for pnt in bankFurnance_coords.keys() if pnt[0] == minx]
                    # print(f"pnt[0]={pnt[0]}\npoints:{bankFurnance_coords.keys()}")
                    get_markedtile_coords(pnt[0])
                except Exception as e:
                    print(f"No points found on screen\nAssuming bank is open\n{e}")
                    return
                sleep(self.path_len)

                if self.Game.isBankOpen():
                    return
                # Loop until bank found
                else:
                    print("Bank was not found")
                    # False to make it find furnance instead of bank
                    self.bank = True
                    continue

            # Clicks on marked furnance tile
            else:
                if self.Game.isCraftWinOpen():
                    print("Craft window was opened")
                    self.bank = True
                    # goes on to smelt window
                    return
                else:
                    if self.Game.isBankOpen():
                        print("Bank window was opened")
                        self.bank = False
                        return

                # clicks on marked furnance
                self.bank = True
                # print(f'self.bank = {self.bank}')
                maxx = max([pnt[0] for pnt in bankFurnance_coords.keys()])
                #print(f'maxx = {maxx}')
                pnt = [pnt for pnt in bankFurnance_coords.keys() if pnt[0] == maxx]
                # print(f"pnt[0]={pnt}\npoints:{bankFurnance_coords.keys()}")
                get_markedtile_coords(pnt[0])
                sleep(self.path_len)
                return
    @decorator
    def depositJewelry(self,*args):
        self.Game.depositAll()
        return
        tries = 0
        while tries < 3:
            bag,bx,by = self.Game.get_bag(True, 'hsv')
            jewlry = self.getJewelInfo('gold')[0]
            low = np.array(jewlry[0])
            high= np.array(jewlry[1])
            mask = cv2.inRange(bag,low,high)

            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #  Boudning rectangle
            # items to deposit
            depositable = {}
            try:
                for cnt in contours[::-1]:
                    # creates a white rectangle around items
                    # x,y,w,h = cv2.boundingRect(cnt)
                    # cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),-1)

                    M = cv2.moments(cnt)
                    # center of bank icon found on minimap
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    rx = int(triangular(-7,7))
                    ry = int(triangular(-10,10))
                    x = cx+rx+bx
                    y = cy+ry+by
                    #print(f"Click interval={rinterval}")
                    #self.Game.hc.move((x,y),duration=self.rinterval('duration'))
                    self.Game.hc.click(x=x,y=y)
                    #print(f"{x,y}")
                    return

            except Exception as e:
                print(e)
                sleep(2)
                continue
            tries += 1
    @decorator
    def withdrawMaterials(self,*args):
        # Taking out item from bank window
        bank, bx, by = self.Game.getBankWindow('hsv')
        #actual jewel like gems
        jewel = self.getJewelInfo(self.jewel)[0]

        low = np.array(jewel[0])
        high= np.array(jewel[1])
        mask = cv2.inRange(bank,low,high)

        # cv2.imshow('mask',mask)
        # cv2.waitKey(1)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #  Boudning rectangle
        try:
            for cnt in contours:
                # creates a white rectangle around items
                # x,y,w,h = cv2.boundingRect(cnt)
                # cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),-1)

                M = cv2.moments(cnt)
                # center of bank icon found on minimap
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                rx = int(triangular(-7,7))
                ry = int(triangular(-10,10))
                x = cx+rx+bx
                y = cy+ry+by
                #self.Game.hc.move((x,y),duration=self.rinterval('duration'))
                self.Game.hc.click(x=x,y=y)
                #print(f"{x,y}")
                break
        except:
            self.terminate = 1
            print(f"No 1st RAW item:{self.jewel}")
        # Gold bar
        obj =  [ [23,224,177],[24,226,220] ]
        # silver bar
        #obj = [[118,17,76],[120,21,185]]
        low = np.array(obj[0])
        high= np.array(obj[1])
        mask = cv2.inRange(bank,low,high)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        try:
            for cnt in contours:
                # creates a white rectangle around items
                # x,y,w,h = cv2.boundingRect(cnt)
                # cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),-1)

                M = cv2.moments(cnt)
                # center of bank icon found on minimap
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                rx = int(triangular(-7,7))
                ry = int(triangular(-10,10))
                x = cx+rx+bx
                y = cy+ry+by
                #self.Game.hc.move((x,y),duration=self.rinterval('duration'))
                self.Game.hc.click(x=x,y=y)
                #print(f"{x,y}")
                # closes bank too fast! slow it DOWN
                sleep(triangular(.3,1))
                break
        except:
            self.terminate = 1
            print(f"No gold bar FOUND!")
    def isItemInBag(self):
        pass
    def smeltWindow(self):
        while 1:
            if self.Game.isCraftWinOpen():
                x,y = self.getJewelInfo(self.jewel)[self.jewelry_type]

                x = x + int(triangular(-5,5))
                y = y + int(triangular(-5,5))
                #self.Game.hc.move((x, y),duration=self.rinterval('duration'))
                self.Game.hc.click(x=x,y=y)
                # makes sure bank is found next if already crafted items
                self.bank = True
                return
            else:
                if self.Game.isBankOpen():
                    return
                print("smelt window was not open\nSelecting furnance again")
                # False to make it find furnance instead of bank
                self.bank = False
                self.backForth(self.terminate)
                continue
    def enableEnergy(self):
        if time()-self.energy_recovery_time > triangular(360,720) and not self.run_energy:
            # this block starts first
            self.path_len = 5
            print(f"path_len={self.path_len}")
            print(f"Clicking toggle run")
            x = self.Game.rsx+570
            y = self.Game.rsy+150
            self.Game.hc.click(x=x,y=y)
            self.energy_recovery_time = time()
    def checkRawMaterials(self,*args):
        pass
def main():
    G = Craft('emerald')
    iteration = 1
    average_time = 0
    while iteration < 100 and not G.terminate:
        start_time = time()
        print("***RUN START***")
        G.backForth(G.terminate)

        print("Depositing Jewlry")
        G.depositJewelry(G.terminate)

        print("Withdrawing materials")
        G.withdrawMaterials(G.terminate)

        print("Closing Bank")
        G.Game.closeBank()

        print("Finding Furnance")
        G.backForth(G.terminate)

        print("Select item to smelt")
        G.smeltWindow()
        n = triangular(43,48)
        sleep(23.5 )
        #sleep(n)
        G.enableEnergy()
        print("***RUN END***")

        elapsed = time() - start_time
        average_time += elapsed
        print(f"\nRun:{iteration} took:{elapsed:.2f} secs...Average:{average_time/iteration:.2f} secs",end=' ')
        print(f"\nJewelry/Hr:{((60*60)/(average_time/iteration)*13):.0f}\nCrafted:{iteration*13} item(s)")
        print(f"Total time:{average_time/60:.2f} mins...\nCurrent Time:{datetime.now():%H:%M:%S\n}")
        iteration += 1

if __name__ == "__main__":
    main()
    # Program to show the use of lambda functions
