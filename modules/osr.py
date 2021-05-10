#!/usr/bin/python3
import cv2
import numpy as np
from pyautogui import press
# Local Modules
from modules import Screenshot
from modules import Keyboard
from modules import setup
from pyclick import HumanClicker
from random import choice,randint,triangular


class Frame():
    def __init__(self,setupwindow=True):
        # object contains window ID and x,y positions
        self.rs_window = setup.Window(setupwindow=setupwindow)
        self.rsx, self.rsy = self.rs_window.position
        self.hc = HumanClicker()
    def closeBank(self):
        """ Keybinding 'esc' should be enabled """
        press('esc', interval=triangular(0.05,0.3))
    def depositAll(self):
        x = self.rsx + int(triangular(432,453))
        y = self.rsy + int(triangular(324,350))
        self.hc.click(x=x,y=y)
    def invCount(self, *args):
        """Counts the number of slots being used in inventory"""
        """pass a func to do something with each slot's ROI, then upper and lower """
        # makes sure inventory button is selected
        # if not self.is_button_selected('inventory'):
        #     self.press_button('inventory')

        bag, bagx,bagy = self.get_bag('bag and coords', 'hsv')
        # HSV range passed in args
        if args:
            low = np.array(args[1])
            high = np.array(args[2])
        # HSV range of Empy Inventory
        else:
            low = np.array([10,46,58])
            high= np.array([21,92,82])
        # applies mask
        mask = cv2.inRange(bag, low, high)

        # only applies to empty inventory
        if not args:
            # removes any noise
            kernel = np.ones((3,3), np.uint8)
            closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            #inverts mask
            closing = cv2.bitwise_not(closing)
        count = 0
        for row in range(7):
            for cols in range(4):
                # 1st Slot ROI
                if row == 0 and cols == 0:
                    #print(row,cols)
                    slot_x = 0
                    slot_x2 = 36

                    slot_y = 0
                    slot_y2 = 43
                # rest of slots ROI
                else:
                    slot_x = row*36+1
                    slot_x2 = (row*36)+36-1

                    slot_y = cols*43+1
                    slot_y2 = 43 + (cols*43)-1

                if args:
                    slot_roi = mask[slot_x:slot_x2, slot_y:slot_y2]
                else:
                    # Selected ROI
                    slot_roi = closing[slot_x:slot_x2, slot_y:slot_y2]

                # Do fucntion with slot_roi else  add to count
                if args:
                    passed_func = args[0]
                    #x,y,_,_ = cv2.boundingRect(slot_roi)
                    #_, psx, psy = getPlayingScreen()
                    slot_x += int(bagx + triangular(1,30))
                    slot_y += int(bagy + triangular(5,25))
                    passed_func(slot_x,slot_y)
                    return

                # just count
                else:
                    # check pixel value == 255
                    if 255 in slot_roi:
                        count += 1

        # returns the N of items in inv
        return count
    def invSlotIter(self):
        # loads database of items to drop
        item_database = {}
        # makes sure inventory button is selected
        if not self.is_button_selected('inventory'):
            self.press_button('inventory')

        bag, bagx,bagy = self.get_bag('bag and coords', 'hsv')
        bag_grey = self.get_bag('only')
        # debug
        #cv2.imshow('bag', bag)
        #cv2.waitKey(0)
        #cv2.imshow('bag_grey', bag_grey)
        #cv2.waitKey(0)

        # HSV range of Empy Inventory
        low = np.array([10,46,58])
        high= np.array([21,92,82])
        # applies mask
        mask = cv2.inRange(bag, low, high)
        #cv2.imshow('mask', mask)
        #cv2.waitKey(0)


        # removes any noise
        kernel = np.ones((3,3), np.uint8)
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        #inverts mask
        closing = cv2.bitwise_not(closing)
        #cv2.imshow('closing', closing)
        #cv2.waitKey(0)

        # finds contours
        #_,contours,_ = cv2.findContours(closing.copy(), 1, 2)

        ### draws white rectangle on found itmes ###
        #for cnt in contours:
        #    # creates a white rectangle around items
        #    x,y,w,h = cv2.boundingRect(cnt)
        #    cv2.rectangle(closing,(x,y),(x+w,y+h),(255,255,255),-1)
        ############################################

        ### Draws division lines ###
        # draws row lines
        #sloth = closing.shape[0] / 7
        #slotw = closing.shape[1] / 4
        #for i,rows in enumerate(xrange(6)):
        #    cv2.line(closing,(0, sloth*(i+1)),(173,sloth*(i+1)),(255,255,255),1)
        # draws col lines
        #for i,cols in enumerate(xrange(3)):
        #    cv2.line(closing,(slotw*(i+1),0),(slotw*(i+1),253),(255,255,255),1)
        ############################

        # checks each slot for white pixels
        count = 0
        for row in range(7):
            for cols in range(4):
                # 1st Slot ROI
                if row == 0 and cols == 0:
                    #print(row,cols)
                    slot_x = 0
                    slot_x2 = 36

                    slot_y = 0
                    slot_y2 = 43
                # rest of slots ROI
                else:
                    slot_x = row*36+1
                    slot_x2 = (row*36)+36-1

                    slot_y = cols*43+1
                    slot_y2 = 43 + (cols*43)-1

                # Selected ROI
                slot_roi = closing[slot_x:slot_x2, slot_y:slot_y2]

                # check pixel value == 255
                if 255 in slot_roi:
                    # getting ROI from original screenshot
                    # bag_roi = bag_grey[slot_x:slot_x2, slot_y:slot_y2]

                    item_database[count] = (slot_x,slot_x2, slot_y, slot_y2)

                    #cv2.imshow('image',bag_roi)
                    #cv2.waitKey(0)
                    count += 1
                else:
                    item_database[count] = 0
                    count += 1

        for img_in_db in item_database:
            print(img_in_db)
            if img_in_db != 0:
                x, x2, y, y2 = img_in_db
                img_in_db = bag_grey[x:x2,y:y2]
                # cv2.imshow('img', img_in_db)
                # cv2.waitKey(0)

        return count
    def open_cw_bank(self):
        """Finds the visiblest square of the chest in castle wars bank, wors better when viewing from above at shortest distance."""

        # Takes screenshot, as Hue-saturated-value image
        play_window,psx,psy = self.getPlayingScreen('hsv')
        lower_gray = np.array([0,0,0])
        upper_gray = np.array([255,255,1])

        # Makes a black/white mask
        mask = cv2.inRange(play_window, lower_gray, upper_gray)
        # inverts selection
        #res = cv2.bitwise_and(play_window, play_window, mask=mask)
        kernel = np.ones((2,2), np.uint8)
        dilation = cv2.dilate(mask, kernel, iterations = 1)

        # cv2.imshow('img', dilation)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # Finds contours
        contours,_ = cv2.findContours(dilation.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        try:
            # looks for center of grey color with biggest area, > 3000
            for con in contours:
                # print(cv2.contourArea(con))
                if cv2.contourArea(con) > 10000:
                    #print(f"big area found {cv2.contourArea(con)}")

                    M = cv2.moments(con)
                    # finds centroid
                    cx,cy = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    psx += cx
                    psy += cy
                    # adds randomness to coords
                    psx += int(triangular(-17,17))
                    psy += int(triangular(-17,17))
                    self.hc.click(x=psx,y=psy)
                    break
        except Exception as e:
            print(f"Bank NOT found!\nMove camera around!\n{e}")
    def find_bank_booth(self):
        """Finds bank booth and clicks it.  Returns True if found, else False"""

        bank_booth_glass_window = ([0,72,149],[179,82,163])
        # take screenshot of playing area
        play_area_screen,psx,psy = self.getPlayingScreen()

        # find glasswindow for bankbooth
        mask = cv2.inRange(play_area_screen, np.array(bank_booth_glass_window[0]), np.array(bank_booth_glass_window[1]))

        # gets osr window's position
        #rsx,rsy = position()

        psx += self.rsx
        psy += self.rsy

        kernel = np.ones((3,3), np.uint8)
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


        #cv2.imshow('img', closing)
        #cv2.waitKey(0)

        # Finds contours
        _,contours,_ = cv2.findContours(closing.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        try:
            for con in contours:
                if cv2.contourArea(con) > 10:
                    #print(cv2.contourArea(con))
                    M = cv2.moments(con)
                    # finds centroid
                    cx,cy = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    psx += cx
                    psy += cy
                    # adds randomness to coords
                    psx += triangular(-7,7)
                    psy += triangular(-7,7)

                    self.hc.click(x=psx,y=psy)
                    sleep(triangular(.1,.5))
                    return 1
        except Exception as e:
            print(f"Bank NOT found!\nMove camera around!\n{e}")
        # returns False if bank not found
        return 0
    def antiban(self, skill):
        #rsx,rsy = position()
        rn =randint(0,99)
        if rn == 0:
            print("Starting antiban")
            # Tuples of locations
            stats_btn = Mouse.genCoords(567,194,589,215)

            #Clicks the skills button
            Mouse.moveClick(stats_btn[0]+self.rsx,stats_btn[1]+self.rsy,1)

            #hovers over a certain skill
            self.skillHover(skill)
            self.moveback(skill)
            return True


            #returns true if antiban ran, to let me know if it acutally did ran

        elif rn == 1:
            print("Starting antiban")
            self.skillsHover(self.rsx,self.rsy)
            self.moveback(skill)
            return True
    def moveback(self, skill):
        if skill == 'magic':
            self.press_button('magic')
        else:
            #moves back to bag
            self.press_button('inventory')
        print("Antiban end")
    def greetings(self, skill):
        n = randint(0,10)
        if randint(0,10):
            if n == 0:
                Keyboard.type_this("What's going on guys?")
            elif n == 1:
                Keyboard.type_this("whats up ppl!?")
            elif n == 2:
                Keyboard.type_this("what you all doing?")
            elif n == 3:
                Keyboard.type_this("hiiiii guys!")
            elif n == 4:
                Keyboard.type_this("what's your guys highest skill lv??")
            elif n == 5:
                Keyboard.type_this("flash1:what!?")
            elif n == 6:
                Keyboard.type_this("what are you talking about?")
            elif n == 7:
                Keyboard.type_this("i dont need to be hearing this")
            elif n == 8:
                Keyboard.type_this("chilling...")
            elif n == 9:
                Keyboard.type_this("skilling, what about you all?")
            elif n == 10:
                Keyboard.type_this("right now im working on {}, what about you guys??".format(skill))

            Keyboard.press('enter')
        sleep(triangular(.1,.5))
    def skillsHover(self, rsx,rsy):
            """Hovers over n skills by n times"""
            n = randint(0,2)
            if n > 0:
                # Tuples of locations
                stats_btn = Mouse.genCoords(567,194,589,215)
                #Clicks the skills button
                Mouse.moveClick(stats_btn[0]+rsx,stats_btn[1]+rsy,1)
                for i in range(n):
                    #                              x1  y1  x2  y2
                    stats_window = Mouse.genCoords(557,234,729,470)
                    # Randomly hovers over a random skill
                    Mouse.moveTo(stats_window[0]+rsx,stats_window[1]+rsy)
                    sleep(triangular(.1,.5))
    def skillHover(self, skill):
        """Hovers over passed skill from 1-5 secs"""
        #Coordinates of skill's button
        skills = {
                'attack':0, 'hitpoints':0,'mining':0,

                'strength':0,'agility':0,'smithing':0,

                'defence':0,'herblore':(620,295,662,311),'fishing':0,

                'ranged':0,'thieving':0,'cooking':0,

                'prayer':0,'crafting':(621,358,664,373),'firemaking':0,

                'magic':(557,388,602,402),'fletching':(620,389,666,406),'woodcutting':0,

                'runecraft':0,'slayer':0,'farming':0,

                'construction':0,'hunter':0
                }

        x1,y1,x2,y2 =skills[skill]
        x,y = Mouse.genCoords(x1,y1,x2,y2)
        # Mouse.moveTo(x,y)
        randS = triangular(.1,.5)
        self.hc.move((x,y),randS)
    def logout(self):
        #  Door Button
        x,y = Mouse.genCoords(636,495,650,515)
        x += self.rsx
        y += self.rsy
        Mouse.moveClick(x,y,1)

        # Log out Button
        x,y = Mouse.genCoords(581,428,707,450)
        x += self.rsx
        y += self.rsy
        Mouse.moveClick(x,y,1)
    def press_button(self, button, *args):
        """Presses button on random coordinates stored in the buttons dictionary.  Returns button coords if 'coors' passed as argument"""
        buttons = {
                'combat':0,
                'stats':(570,197,586,214),
                'quest':0,
                'inventory':(631,194,658,221),
                'equipment':(666,196,687,216),
                'prayer':(700,198,720,214),
                'magic':(733,195,751,214),
                'clan':0,
                'friend':0,
                'enemy':0,
                'logout':0,
                'options':0,
                'emotes':0,
                'music':0,
                'quick-prayer':0,
                'run':0
                }

        #unpacks the tuple
        x1,y1,x2,y2 = buttons[button]

        try :
            if args[0] == 'coords':
                return x1,y1,x2,y2
        except:
            pass

        #generates random coords
        x,y = Mouse.genCoords(x1,y1,x2,y2)
        #moves to those coords
        Mouse.moveClick(x,y,1)
    def findOptionClick(self, x,y,option_name):
            #Mouse.moveClick(x, y, 3)
            print(f"Right-Clicking:x{x} y:{y}")
            self.hc.click(x=x,y=y)
            sleep(triangular(.5,1))
            """Option name of in Image database only needs to be passed, x,y are obsoleate"""
            from modules import Imgdb
            # Image DB
            idb = Imgdb.ImgDb()
            #name of option loaded from image db
            template = idb.pickled_dict[option_name]
            # turning template to graysacle if RBG
            if len(template.shape) == 3:
                template = cv2.cvtColor(template,cv2.COLOR_RGB2GRAY)
            # getting w and h for generating random coords in range
            template_w, template_h = template.shape[::-1]

            rs_window, x, y = self.getPlayingScreen('gray')


            res = cv2.matchTemplate(rs_window,template,cv2.TM_CCOEFF_NORMED)
            threshold = 1
            # Store the coordinates of matched area in a numpy array
            loc = np.where( res >= threshold)

            # clicks on option here when found in pattern
            for pt in zip(*loc[::-1]):#goes through each found image
                # Draw a rectangle around the matched region.
                # cv2.rectangle(rs_window, pt, (pt[0] + template_w, pt[1] + template_h), (0,255,255), 2)

                # creates list of possible coords
                ptx = [i for i in range(pt[0]+5, pt[0] + template_w)]
                pty = [i for i in range(pt[1]+5, pt[1] + template_h)]
                # chooses a single coords from the list
                ptx = choice(ptx)
                pty = choice(pty)
                print(f"ptx{ptx} pty{pty}")

                # debug ###
                #cv2.imshow('img', rs_window)
                #cv2.waitKey(5000)
                #cv2.destroyAllWindows()

                # range of x and y to click on.
                # in the options
                #Mouse.randMove(x,y1,x+(w/2),y2, 1)
                #ptx, pty = Mouse.randCoord(pt, template_w, template_h)
                #Mouse.moveClick(ptx,pty, 1)
                self.hc.click(x=ptx,y=pty)
                sleep(triangular(1,2))
                break
    def position(self, windowID=''):
        """ Returns top left position of Runescape window"""
        return self.rsx, self.rsy
    def getPlayingScreen(self, color):
        """ Returns play screen area as an HSV image,
            and the first point of the image """

        #playScreen = Screenshot.shoot(self.rsx, self.rsy,517,362,color)
        playScreen = Screenshot.shoot(self.rsx, self.rsy,760,520,color)

        return playScreen, self.rsx, self.rsy
    def getMinimap(self):
        """ INCOMPLETE Returns minimap area as an HSV image,
            and the first point of the image """
        # bag postions, x1,y1-x2,y2
        x1 = self.rsx + 570
        y1 = self.rsy + 30
        x2 = self.rsx + 720
        y2 = self.rsy + 170
        minimap = Screenshot.shoot(x1,y1,x2,y2,'hsv')
        return minimap,x1, y1
    def get_bag(self, return_coords=False, *args):
        #x1, y1 = position() #Get runescapes top-left coords

        # bag postions, x1,y1-x2,y2
        x1 = self.rsx + 565
        y1 = self.rsy + 239
        x2 = self.rsx + 721
        y2 = self.rsy + 485

        try: # block to allow this func to also get 'hsv' img objects
            for arg in args:
                if arg == 'hsv':
                    rs_bag = Screenshot.shoot(x1,y1,x2,y2,'hsv')
                    return rs_bag, x1, y1
                if arg == 'gray':
                    rs_bag = Screenshot.shoot(x1,y1,x2,y2)
                    return rs_bag, x1, y1
        except:
            pass

        rs_bag = Screenshot.shoot(x1,y1,x2,y2)

        if return_coords:
            return rs_bag, x1, y1
        else:
            return rs_bag
    def getBankWindow(self, *args):
        """ window only includes the items in bank, to tabs or buttons"""
        #creates bank window boundaries
        x1 = self.rsx + 70
        y1 = self.rsy + 105
        x2 = self.rsx + 440
        y2 = self.rsy + 319
        # passing 'hsv' to this function returns hsv image
        try:
            if args[0] == 'hsv':
                #gets screenshot object
                bankWindow = Screenshot.shoot(x1,y1,x2,y2, 'hsv')
                ##### DEBUG
                #cv2.imshow('bankwindow', bankWindow)
                #cv2.waitKey(0)
                ####
                return bankWindow, x1, y1
        except:
            #gets screenshot object
            bankWindow = Screenshot.shoot(x1,y1,x2,y2)
            return bankWindow, x1, y1
    def isBankOpen(self):
        """checks to see if bank is open, returns True, else False"""
        # black X button hsv values
        buttonx_hsv = (np.array([0,254,0]),np.array([179,255,255]))
        # gets current game's position
        #self.rsx,rsy = self.position()
        #button X on bank window coords
        x1 = self.rsx+484
        y1 = self.rsy+44
        x2 = self.rsx+497
        y2 = self.rsy+59

        # Screenshot X button
        img = Screenshot.shoot(x1,y1,x2,y2,'hsv')
        # cv2.imshow('img', img)
        # cv2.waitKey(2000)
        # cv2.destroyAllWindows()
        # Apply hsv ranges
        mask = cv2.inRange(img,buttonx_hsv[0], buttonx_hsv[1])

        # counts white pixels in X
        counter = 0
        for colors in mask:
            for color_value in colors:
                if color_value == 255:
                    counter += 1
        #print(counter)
        #cv2.imshow('img', mask)
        #cv2.waitKey(0)
        # 54 = Bank is open
        if counter == 54:
            return True
        return False
    def isCraftWinOpen(self):
        """checks to see if bank is open, returns True, else False"""
        # black X button hsv values
        buttonx_hsv = (np.array([0,254,0]),np.array([179,255,255]))
        # gets current game's position
        #self.rsx,rsy = self.position()
        #button X on bank window coords
        x1 = self.rsx+480
        y1 = self.rsy+53
        x2 = self.rsx+497
        y2 = self.rsy+70

        # Screenshot X button
        img = Screenshot.shoot(x1,y1,x2,y2,'hsv')
        # Apply hsv ranges
        mask = cv2.inRange(img,buttonx_hsv[0], buttonx_hsv[1])
        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imshow('mask', mask)
        # cv2.waitKey(00)
        # cv2.destroyAllWindows()

        # counts white pixels in X
        counter = 0
        for colors in mask:
            for color_value in colors:
                if color_value == 255:
                    counter += 1
        #cv2.imshow('img', mask)
        #cv2.waitKey(0)
        # 54 = Bank is open
        # uncomment to see the number to set it to
        # print(counter) # uncomment to show what number should be on next line
        if counter == 54:
            return True
        return False
    def isRunActive(self):
        """checks to see if run is active, returns True, else False"""
        # checking color yellow on boot
        run_icon = (np.array([25,135,236]),np.array([26,145,237]))
        x1 = self.rsx+564
        y1 = self.rsy+152
        x2 = self.rsx+578
        y2 = self.rsy+160

        img = Screenshot.shoot(x1,y1,x2,y2,'hsv')
        # Apply hsv ranges
        mask = cv2.inRange(img,run_icon[0], run_icon[1])
        # if true run is off
        if mask.any():
            return True
        else:
            return False
    def isInvEmpty(self,bagimg=0):
        bag, bagx,bagy = self.get_bag('bag and coords', 'hsv')
        # looks for color of empty inv
        low = np.array([10,46,58])
        high= np.array([21,92,82])
        # applies mask
        mask = cv2.inRange(bag, low, high)
        # removes any noise
        kernel = np.ones((5,5), np.uint8)
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow('img', closing)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        if bagimg == 0:
            # looks to see if the inv is all white pixels
            # returns true, else False
            if (closing.view() == 255).all():
                # print("Inventory is Empty")
                return True
            # print("Inventory is Full")
            return False
        if bagimg == 1:
            # looks to see if the inv is all white pixels
            # returns true, else False
            if (closing.view() == 255).all():
                # print("Inventory is Empty")
                return True, (bag, bagx, bagy)
            # print("Inventory is Full")
            return False, (bag, bagx, bagy)
    def is_button_selected(self, button_name):
        """Returns true if button is selected, else False"""
        x1, y1, x2, y2 = self.press_button(button_name, 'coords')
        button_img = Screenshot.shoot(x1,y1,x2,y2, 'hsv')
        lower_red = np.array([0, 179, 0])
        upper_red = np.array([4, 193, 255])

        mask = cv2.inRange(button_img, lower_red, upper_red)

        for colors in mask:
            for value in colors:
                if value == 255:
                    #print('{} is selected'.format(button_name))
                    return 1
        # print('{} is NOT selected'.format(button_name))
        return 0
if __name__ == '__main__':
    osrs = Frame()
    osrs.isInvEmpty()
