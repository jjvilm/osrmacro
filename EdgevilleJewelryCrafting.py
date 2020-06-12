#!/bin/python3
import cv2
import numpy as np
from modules import Screenshot, RS
#from pyautogui import click
from random import randint, random
from time import sleep,time


class Craft():
    def __init__(self,jewel):
        self.Game = RS.Osr_game()
        self.jewel = jewel
        self.bank = True
        self.path_len = 10
        self.run_energy = False
        self.duration = 0.05
        self.energy_recovery_time = time()
    def getJewelInfo(self,*args):
        print(args)
        jewels = {  'diamond':([[0,4,168],[1,6,169]],
                        (self.Game.rsx + 270,self.Game.rsy + 190)),
                    'ruby':([[0,227,79],[4,245,99]],
                        (self.Game.rsx + 220,self.Game.rsy + 192)),
                    'emerald':([[56,202,188],[57,223,189]],
                        (self.Game.rsx + 160, self.Game.rsy + 130)),#emerald ring coords
                    'necklace':([[0,204,0],[26,235,255]]),
                        }
        return jewels[args[0]]
    def backForth(self):
        if self.Game.isRunActive():
            self.path_len = 5
            print(f"Run is ACTIVE, length={self.path_len} secs")
        else:
            self.path_len = 10
            print(f"Run is NOT ACTIVE, length={self.path_len} secs")
        def get_markedtile_coords(pnt):
            x,y = pnt
            rinterval = self.rinter()
            #print(f"Click interval={rinterval}")
            self.Game.hc.move((x,y),duration=self.duration + random())
            self.Game.hc.click(interval=rinterval)
            #print(f"{x,y}")
            return
        while 1:
            game_scrn, sx, sy = self.Game.getPlayingScreen('hsv')
            marked_tile = [ [153,208,145],[155,255,255] ]
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
                try:
                    M = cv2.moments(cnt)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    rx = randint(-1,1)
                    ry = randint(-1,1)
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
                print(f'self.bank = {self.bank}')
                # Do if bank open
                print("Found bank booth")
                minx = min([pnt[0] for pnt in bankFurnance_coords.keys()])
                pnt = [pnt for pnt in bankFurnance_coords.keys() if pnt[0] == minx]
                print(f"pnt[0]={pnt[0]}\npoints:{bankFurnance_coords.keys()}")
                get_markedtile_coords(pnt[0])
                sleep(self.path_len + random())

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
                self.bank = True
                print(f'self.bank = {self.bank}')
                maxx = max([pnt[0] for pnt in bankFurnance_coords.keys()])
                #print(f'maxx = {maxx}')
                pnt = [pnt for pnt in bankFurnance_coords.keys() if pnt[0] == maxx]
                print(f"pnt[0]={pnt}\npoints:{bankFurnance_coords.keys()}")
                get_markedtile_coords(pnt[0])
                sleep(self.path_len + random())
                return
    def depositJewelry(self):
        while 1:
            bag,bx,by = self.Game.get_bag(True, 'hsv')
            jewlry = self.getJewelInfo('necklace')
            low = np.array(jewlry[0])
            high= np.array(jewlry[1])
            mask = cv2.inRange(bag,low,high)

            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #  Boudning rectangle
            for cnt in contours[::-1]:
                try:
                    # creates a white rectangle around items
                    # x,y,w,h = cv2.boundingRect(cnt)
                    # cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),-1)

                    M = cv2.moments(cnt)
                    # center of bank icon found on minimap
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    rx = randint(-1,1)
                    ry = randint(-1,1)
                    x = cx+rx+bx
                    y = cy+ry+by
                    rinterval = self.rinter()
                    #print(f"Click interval={rinterval}")
                    self.Game.hc.move((x,y),duration=self.duration + random())
                    self.Game.hc.click(interval=rinterval)
                    #print(f"{x,y}")
                    return
                except Exception as e:
                    print(e)
                    sleep(1)
                    continue
    def withdrawMaterials(self):
        # Taking out item from bank window
        bank, bx, by = self.Game.getBankWindow('hsv')

        jewel = self.getJewelInfo(self.jewel)[0]

        low = np.array(jewel[0])
        high= np.array(jewel[1])
        mask = cv2.inRange(bank,low,high)

        # cv2.imshow('mask',mask)
        # cv2.waitKey(1)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #  Boudning rectangle
        for cnt in contours:
            # creates a white rectangle around items
            # x,y,w,h = cv2.boundingRect(cnt)
            # cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),-1)

            M = cv2.moments(cnt)
            # center of bank icon found on minimap
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            rx = randint(-1,1)
            ry = randint(-1,1)
            x = cx+rx+bx
            y = cy+ry+by
            rinterval = self.rinter()
            #print(f"Click interval={rinterval}")
            self.Game.hc.move((x,y),duration=self.duration + random())
            self.Game.hc.click(interval=rinterval)
            #print(f"{x,y}")
            break
        # Gold bar
        obj =  [ [23,224,177],[24,226,220] ]
        low = np.array(obj[0])
        high= np.array(obj[1])
        mask = cv2.inRange(bank,low,high)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours[::-1]:
            # creates a white rectangle around items
            # x,y,w,h = cv2.boundingRect(cnt)
            # cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),-1)

            M = cv2.moments(cnt)
            # center of bank icon found on minimap
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            rx = randint(-1,1)
            ry = randint(-1,1)
            x = cx+rx+bx
            y = cy+ry+by
            rinterval = self.rinter()
            #print(f"Click interval={rinterval}")
            self.Game.hc.move((x,y),duration=self.duration + random())
            self.Game.hc.click(interval=rinterval)
            #print(f"{x,y}")
            break
    def smeltWindow(self):
        while 1:
            if self.Game.isCraftWinOpen():
                x,y = self.getJewelInfo(self.jewel)[1]

                x = x + randint(-10,10)
                y = y + randint(-10,10)

                rinterval = self.rinter()
                #print(f"Click interval={rinterval}")
                self.Game.hc.move((x, y),duration=self.duration + random())
                self.Game.hc.click(interval=rinterval)
                return
            else:
                print("smelt window was not open\nSelecting furnance again")
                # False to make it find furnance instead of bank
                self.bank = False
                self.backForth()
                continue
    def enableEnergy(self):
        if time()-self.energy_recovery_time > 100:
            # this block starts first
            if not self.run_energy:
                self.path_len = 5
                print(f"path_len={self.path_len}")
                print(f"Enabling energy")
                self.run_energy = True
                self.Game.hc.click(x=self.Game.rsx+570,y=self.Game.rsy+150,interval=random())
                self.energy_recovery_time = time()
                sleep(random())
            # then this one, then switch back on next iter
            else:
                # slows down when out of energy
                self.path_len = 10
                print(f"path_len={self.path_len}")
                self.run_energy = False
                self.energy_recovery_time = time()
    def rinter(self):
        r = 0
        while (r > 0.25) or (r < 0.075):
            r = random()
        return r

def main():
    G = Craft('emerald')
    iteration = 1
    while iteration < 100:
        start_time = time()
        #x.enableEnergy()

        # Clicks on bank marked tile
        sleep(random())
        print("Loop START:\nOpening bank...")
        G.backForth()

        print("Depositing Jewlry")
        G.depositJewelry()

        print("Withdrawing materials")
        G.withdrawMaterials()

        print("Clsing Bank")
        G.Game.closeBank()
        sleep(random())

        print("Finding Furnance")
        G.backForth()

        print("Select item to smelt")
        G.smeltWindow()
        sleep(23 + random())

        print(f"\nIteraion:{iteration} took:{time()-start_time:.2f} secs...\n")
        iteration += 1


if __name__ == "__main__":
    main()
    # Program to show the use of lambda functions
