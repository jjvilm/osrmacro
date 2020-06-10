#!/bin/python3
import cv2
import numpy as np
from modules import Screenshot, RS
#from pyautogui import click
from random import randint, random
from time import sleep,time


class Craft():
    def __init__(self):
        self.Game = RS.Osr_game()
        self.bank = True
        self.walk_speed = 8
        self.run_energy = True
        self.energy_recovery_time = time()
    def backForth(self):
        def get_markedtile_coords(pnt):
            x,y = pnt
            rinterval = random() / 2
            #print(f"Click interval={rinterval}")
            self.Game.hc.move((x,y),duration=random())
            self.Game.hc.click(interval=rinterval)
            #print(f"{x,y}")
            return

        game_scrn, sx, sy = self.Game.getPlayingScreen('hsv')
        marked_tile = [ [153,208,145],[155,255,255] ]
        low = np.array(marked_tile[0])
        high= np.array(marked_tile[1])
        mask = cv2.inRange(game_scrn,low,high)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # get smaller values in x to keep bank on left
        bankFurnance_coords = {}
        for cnt in contours:
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            rx = randint(-3,3)
            ry = randint(-3,3)
            x = cx+rx+sx
            y = cy+ry+sy
            bankFurnance_coords[(x,y)] = M
        # clicks on marked bank tile
        if self.bank:
            self.bank = False
            while 1:
                if not self.Game.isBankOpen():
                    #print("Found bank")
                    minx = min([pnt[0] for pnt in bankFurnance_coords.keys()])
                    pnt = [pnt for pnt in bankFurnance_coords.keys() if pnt[0] == minx]
                    print(f"pnt[0]={pnt[0]}")
                    get_markedtile_coords(pnt[0])
                    sleep(self.walk_speed + random())
                elif self.Game.isBankOpen():
                    #print("Bank opened")
                    return
    # Clicks on marked furnance tile
        else:
            self.bank = True
            maxx = max([pnt[1] for pnt in bankFurnance_coords.keys()])
            pnt = [pnt for pnt in bankFurnance_coords.keys() if pnt[1] == maxx]
            print(f"pnt[0]={pnt[0]}")
            # #print(f"\nMax X pnt:{pnt[0]}\ninDict:{bankFurnance_coords.keys()}\n")
            get_markedtile_coords(pnt[0])
            sleep(self.walk_speed + random())
    def depositJewelry(self):
        while 1:
            bag,bx,by = self.Game.get_bag(True, 'hsv')
            jewlry = [ [0,204,0],[26,235,255] ]
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
                    rx = randint(-3,3)
                    ry = randint(-3,3)
                    x = cx+rx+bx
                    y = cy+ry+by
                    rinterval = random() / 2
                    #print(f"Click interval={rinterval}")
                    self.Game.hc.move((x,y),duration=random())
                    self.Game.hc.click(interval=rinterval)
                    #print(f"{x,y}")
                    return
                except Exception as e:
                    #print(e)
                    sleep(1)
                    continue
    def withdrawMaterials(self):
        bank, bx, by = self.Game.getBankWindow('hsv')

        # ruby
        obj = [ [0,227,79],[4,245,99] ]
        low = np.array(obj[0])
        high= np.array(obj[1])
        mask = cv2.inRange(bank,low,high)

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
            rx = randint(-3,3)
            ry = randint(-3,3)
            x = cx+rx+bx
            y = cy+ry+by
            rinterval = random() / 2
            #print(f"Click interval={rinterval}")
            self.Game.hc.move((x,y),duration=random())
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
            rx = randint(-3,3)
            ry = randint(-3,3)
            x = cx+rx+bx
            y = cy+ry+by
            rinterval = random() / 2
            #print(f"Click interval={rinterval}")
            self.Game.hc.move((x,y),duration=random())
            self.Game.hc.click(interval=rinterval)
            #print(f"{x,y}")
            break
    def smeltWindow(self):
        x = self.Game.rsx + 220
        y = self.Game.rsy + 192

        rx = randint(-2,2)
        ry = randint(-2,2)

        rinterval = random() / 2
        #print(f"Click interval={rinterval}")
        self.Game.hc.move((x+rx, y+ry),duration=random())
        self.Game.hc.click(interval=rinterval)
    def enableEnergy(self):
        # after 6 mins tun on run energy
        if time() - self.energy_recovery_time > 600:

            if not self.run_energy:
                self.walk_speed = 8
                self.run_energy = True
            else:
                print(f"Enabling energy")
                self.walk_speed = 6
                self.run_energy = False
                self.energy_recovery_time = time()
                self.Game.hc.click(x=self.Game.rsx+570,y=self.Game.rsy+150,interval=random())
                sleep(random())
def main():
    x = Craft()
    while 1:
        start_time = time()
        x.enableEnergy()

        # Clicks on bank marked tile
        print("Opening bank...")
        x.backForth()

        print("Depositing Jewlry")
        x.depositJewelry()

        print("Withdrawing materials")
        x.withdrawMaterials()

        print("Clsing Bank")
        x.Game.closeBank()
        sleep(random())

        print("Finding Furnance")
        x.backForth()

        print("Select item to smelt")
        x.smeltWindow()
        sleep(23 + random())

        print(f"\nRun took:{time()-start_time} secs...\n")


if __name__ == "__main__":
    main()
    # x = Craft()
    # x.findFurnance()

# cv2.imshow('mask', mask)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
