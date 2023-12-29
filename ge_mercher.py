from modules import Screenshot
from modules import Keyboard
from modules import setup
import pyautogui
import cv2
import time
import numpy as np
# import pytesseract
from random import triangular, randint,choice,shuffle
from modules import osr

# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

rs = osr.Frame(setupwindow=False)
markets = {
            'market':['willow logs', 'nature rune', 'death rune', 'raw swordfish',
                    'yew logs', 'cosmic rune', 'gold ore',
                    'lobster','plank','silver ore','jug of wine'],
            'food': ['lobster','raw swordfish','raw salmon','raw tuna'],#all raw
            'log':['logs','oak logs','willow logs','yew logs'],
            'metal':['bronze bar','iron bar', 'steel bar', 'gold bar',
                    'mithril bar','adamantite bar', 'runite bar'],
            'rune':['law rune', 'nature rune', 'death rune', 'cosmic rune',
                    'chaos rune',],
            'raids':['rune scimitar','rune platebody', 'rune platelegs',
                    'rune full helm','rune med helm','rune chainbody',
                    'iron arrow','steel arrow','bronze arrow'],
            'herb':['grapes'],
            'potion':['vial','strength potion(3)','vial of water'],
            'botfarm':['adamantite bar','iron ore','mithril bar',
                        'nature rune','raw lobster',
                        'raw swordfish','runite bar','steel bar',
                        'wine of zamorak', 'yew logs'],
            'longterm':['maple logs','body rune', 'fire rune', 'earth rune',
                        'water rune', 'air rune', 'pure essence','rune essence',
                        'bucket'],
            'fastflips':['law rune', 'nature rune', 'death rune','chaos rune']
}
def getItemList():
    market = choice(markets['market'])
    food = choice(markets['food'])
    log = choice(markets['log'])
    metal = choice(markets['metal'])
    rune = choice(markets['rune'])
    raids = choice(markets['raids'])
    herb = choice(markets['herb'])
    potion = choice(markets['potion'])
    botfarm = choice(markets['botfarm'])
    longterm = choice(markets['longterm'])
    fastflips = choice(markets['fastflips'])

    return [market, food, log, rune, botfarm,botfarm,botfarm,fastflips]

# notallowlist = ['maple logs','jug', 'mind rune', 'fire rune', 'earth rune',
#                 'air rune', 'water rune','raw lobster','chaos rune','lobster'
#                 'yew logs', 'willow logs', 'vial','vial of water',]


# items = [item for item in items if item not in notallowlist]
items = getItemList()

# pick 3 random items from list above
unique_set = set()
for i,ele in enumerate(items):
    unique_set.add(items[i])
items = unique_set


print(f"Price checking these items...:\n{items}")


def getitemhsv(itemname):
    items = {'willow logs':[[24,160,78],[25,175,87]],
            'oak logs':[[17,135,105],[18,140,149]],
            'nature rune':[[54,19,116],[63,234,155]],
            'death rune':[[0,0,207],[6,9,255]],
            'swordfish':[[144,63,104],[148,131,224]],
            'yew logs':[[21,222,59],[23,253,102]],
            'maple logs':[[19,224,107],[20,235,125]],
            'cosmic rune':[[30,209,207],[39,226,234]],
            'coal':[[27,63,39],[41,99,52]],
            'iron ore':[[8,124,48],[9,163,80]],
            'lobster':[[14,219,143],[16,245,245]],
            'gold ore':[[14,98,98],[28,230,217]],
            }
    if itemname in items.keys():
        return items[itemname]
    else:
        return [[0,0,0],[0,0,0]]

class GE_Trading():

    def __init__(self, cash=0):
        # below is tuple w/ 4 elements: x, y , w, h
        self.pos = (0,0,500,500)
        self.cash = cash
        # clicks for when buying above or below market price @+5%
        self.clicks = int(triangular(5,20))
        self.wbc = (.5,1.3)
        self.item_stat = {}
        self.idle = True
    def rndWait(self,*args):
        initial = self.wbc[0]
        wait = self.wbc[1]
        if args:
            initial = args[0]
            wait = args[1]
        duration = triangular(initial,wait)
        # print(f"Sleeping for:{duration}")
        time.sleep(duration)
    def _setCash(self):
        if self.cash == 0:
            self.cash = int(input("Enter goldcoin amount:\n"))
    def get_slots(self, buysell):
        """ Returns available buy/sell slot location by x, y, w, h """
        # gets trading window pos
        x, y, w, h = self.pos
        # find buy/sell slots
        img = Screenshot.this(x, y, w, h, 'hsv')

        if buysell == 'buy':
            low = [32,248,192]
            high = [35,254,203]
        elif buysell == 'sell':
            low = [16,248,122]
            high = [17,251,204]

        available_slots = self.get_hsv_pattern_pos(img, low, high)

        slots = list()
        for cnt in available_slots:
            rect = cv2.boundingRect(cnt)
            #pyautogui.moveTo(x, y)
            slots.append(rect)
        return slots #positions of buy/sell arrows
    def get_hsv_pattern_pos(self, image=None,low_hsv=None,high_hsv=None):
        """Returns contours of location pattern is found"""
        low_hsv = np.array(low_hsv)
        high_hsv = np.array(high_hsv)
        mask = cv2.inRange(image, low_hsv, high_hsv)

        contours, h = cv2.findContours(mask, 1, 2)
        return contours
    def set_main_wndw(self):
        """ Finds the GE trading window when slots are visible """
        # gets screen size
        w, h = pyautogui.size()
        # takes screen screenshot. Returns  hsv format image
        scrn_scrnshot = Screenshot.this(0, 0, w, h, 'hsv')

        # find Grand exchange window
        # the  rectangle only the GE can have when GE Trading window active
        lower_hsv = np.array([12, 0, 7])
        upper_hsv = np.array([40, 62, 64])
        # mask of applied values
        mask = cv2.inRange(scrn_scrnshot, lower_hsv, upper_hsv)

        # find contours to get sides of rectangle
        contours, h = cv2.findContours(mask, 1, 2)

        for cnt in contours:
            # looks for biggest square
            # if cv2.contourArea(cnt) <= 1695.0:
            #    continue
            # checks contour sides
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

            # Squares are found with this code
            # to find the rectangular GE window
            if len(approx) == 4:
                if cv2.contourArea(cnt) == 140123:
                    # position of GE Trading window found
                    x, y, w, h = cv2.boundingRect(cnt)
                    # add to take screenshot of GE trading window
                    w = x + w
                    h = y + h
                    self.pos = (x, y, w, h)
                    print(f"Trading window at:X={self.pos[0]} Y={self.pos[1]}")
                    return
        else:
            print("Finished successfully")
    def clickArea(self,pnt,w,h):
        """ Returns random coords from area of pnt based
            on its width and height'"""
        x = pnt[0] + int(triangular(1,w))
        y = pnt[1] + int(triangular(1,h))
        return x,y
    def buySellItem(self,action,itemname,qty=1,price=0):
        """ gives option to 'buy' 'sell', mainly for 'buy' """
        slots = self.get_slots(action)
        try:
            ## picks random slot from buy/sell slots
            n = randint(0,len(slots) - 1)
        except:
            print("Go back to slot selection")
            print("Find back button and click")
            return
        ## combines coords
        pos = slots[n]
        x = pos[0] + self.pos[0] - 16 #to adjust area of click
        y = pos[1] + self.pos[1] #15
        # ## adds randomness
        self.clickArea((x,y),38,25)

        # clicks on buy or sell icon
        rs.hc.click(x=x,y=y)
        self.rndWait(2,3)
        # time.sleep(3)

        # types in items' name
        if action == 'buy':
            print(f"\nANALYZING: {itemname}...")
            Keyboard.write(itemname)
        # selects item to buy
        self.rndWait()
        x,y = self.clickArea((18,397),150,23)
        rs.hc.click(x=x ,y=y)
        self.rndWait()
        # checks to se if buying multiple qty
        if qty == 1:
            # buy @5%. clicks
            x,y = self.clickArea((440,233),28,20)
            rs.hc.click(x=x ,y=y,clicks=self.clicks)
            self.confNcoll()
            self.rndWait()
            return
        # types n quantiy of item
        x,y = self.clickArea((231,234),24,13)
        rs.hc.click(x=x ,y=y)
        self.rndWait(.5,1)
        Keyboard.write(str(int(qty)))
        self.rndWait(.1,.7)
        Keyboard.press('enter')
        self.rndWait(.5,1)
        #clicks on enter price
        x,y = self.clickArea((386,231),24,13)
        rs.hc.click(x=x ,y=y)
        self.rndWait()
        Keyboard.write(str(int(price)))
        self.rndWait(.3,.7)
        Keyboard.press('enter')
        self.confNcoll(coll=False,transaction=False)


    def checkTransaction(self):
        # waits until item transaction is complete
        while 1:
            # green complete bar hsv values
            low = np.array([59,250,95])
            high = np.array([60,255,96])
            window,_,_ = rs.getPlayingScreen('hsv')
            mask = cv2.inRange(window, low, high)

            # cv2.imshow('mask',mask)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            contours,_ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            try:
                # breaking only if complete transcation
                for con in contours:
                    # print("Found complete transaction")
                    return 1
                #return 1 # trans found returning value
            except Exception as e:
                # if it waits too long, move on to diff item cancel current
                print(e)
                self.rndWait(.5,1)
                continue
    def confNcoll(self,conf=True,coll=True,transaction=True):
        """ clicks on confirm button then on collect button """
        # clicks confirm
        if conf:
            self.rndWait()
            x,y = self.clickArea((195,302),143,30)
            rs.hc.click(x=x ,y=y)
            self.rndWait(1,2)
        # waits until item transaction is complete
        if transaction:
            self.checkTransaction()
        # clicks on collect
        if coll:
            x,y = self.clickArea((418,87),76,15)
            rs.hc.click(x=x ,y=y)
    def sellItem(self,itemname):
        """ select 1st item from bag and clicks it to sell, then confirm and coll """
        def click(x,y):
            """ Used as a passable func for invCount"""
            # print(f"Clicking ({x,y})")
            rs.hc.click(x=x,y=y)

        low, high = getitemhsv(itemname)

        rs.invCount(click,low,high)

        # give time for sell window to come up
        self.rndWait(1,2)
        #click @-5%
        x,y = self.clickArea((284,233),27,20)
        rs.hc.click(x=x ,y=y,clicks=self.clicks)

        self.confNcoll()
    def readHistory(self,itemaction):
        def singles(buysell):
            x1 = 360
            w = 40
            h = 14
            if buysell == 's':
                # finds line of text where price is displayed when sold
                #PIL format as RGB
                y1 = 98
                return pyautogui.screenshot(region=(x1,y1,w,h)) #X1,Y1,X2,Y2
            elif buysell == 'b':
                # finds line of text where price is displayed when bought
                #PIL format as RGB
                y1 = 136
                return pyautogui.screenshot(region=(x1,y1,w,h)) #X1,Y1,X2,Y2
        def mults():
            #PIL format as RGB
            x1 = 360
            y1 = 107
            w = 100
            h = 11
            return pyautogui.screenshot(region=(x1,y1,w,h)) #X1,Y1,X2,Y2

        # image ROI where price resides
        img = singles(itemaction)
        img = np.array(img)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        cv2.imshow('img',gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # Blur and perform text extraction
        # thresh = cv2.GaussianBlur(gray, (1,1), 0)
        thresh = 255 - cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # cv2.imshow('img',thresh)
        # cv2.waitKey(500)
        # cv2.destroyAllWindows()

        digits = ''
        contours,_ = cv2.findContours(thresh.copy(), 1, 2)
        last_pnt = 0
        for cnt in contours[::-1]:
            # block makes sure number read once after reading last char
            if last_pnt == 0:
                last_pnt = cnt[0][0][0]
            else:
                if last_pnt > cnt[0][0][0]:
                    continue
                last_pnt = cnt[0][0][0]


            x,y,w,h = cv2.boundingRect(cnt)

            scoot = 0
            x1 = x - scoot
            y1 = y - scoot
            x2 = x + w + scoot
            y2 = y + h + scoot
            # creates a white rectangle around items
            ROI = thresh[y1:y2, x1:x2]

            # print("cnt[0],cnt[-1]",cnt[0],cnt[-1])
            # cv2.imshow('single_char_roi',ROI)
            # cv2.waitKey(200)
            # cv2.destroyAllWindows()

            # read_txt = pytesseract.image_to_string(ROI, config=custom_config)
            digit = self.getDigit(ROI)
            # print("God digit", digit,"type",type(digit))
            if digit == -1:
                continue
            # cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),1)
            digits += str(digit)
        # cv2.imshow('single_char_roi',img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        try:
            digits = int(digits)
            return digits
        except:
            print("something happenned...No numbers found.  check screenshots")
            return 0

    def getMargin(self,itemname):
        self.buySellItem('buy',itemname)
        self.rndWait(.5,1)
        self.sellItem(itemname)
        # clicks on history button in GE window
        self.rndWait()
        x,y = self.clickArea((32,57),40,12)
        rs.hc.click(x=x ,y=y)
        # give time for buysell history to come up
        self.rndWait(2,3)
        #reads the prices on history
        # bought price
        hp = self.readHistory('b')
        print(f"\tHIGH: {hp} gc")
        lp = self.readHistory('s')
        margin = hp - lp
        print(f"\t LOW: {lp} gc")
        roi = (margin/lp)*100
        print(f"\tMRGN: {margin} gc\tROI= {roi:.2f}%")

        # Add entries to item's stat
        self.item_stat[itemname] = {}
        self.item_stat[itemname]['margin'] = margin
        self.item_stat[itemname]['low'] = lp
        self.item_stat[itemname]['high'] = hp
        self.item_stat[itemname]['roi'] = roi

        # click on Exchange to go buy to buy/buysell
        x,y = self.clickArea((45,57),47,11)# pnt, w h
        rs.hc.click(x=x ,y=y)
        self.rndWait(1,2)
    def collMargins(self,itemList):
        for item in itemList:
            self.getMargin(item)
    def getDigit(self,roi):
        """ Pass roi of digit to match against embadded database
        to return digit as int or -1 if not a digit"""
        digitroi = {'0':[  [  0, 255, 255, 255,   0],
                           [255,   0,   0,   0, 255],
                           [255,   0,   0,   0, 255],
                           [255,   0,   0,   0, 255],
                           [255,   0,   0,   0, 255],
                           [255,   0,   0,   0, 255],
                           [255,   0,   0,   0, 255],
                           [  0, 255, 255, 255,   0]],

                    '1':[  [  0, 255,   0],
                           [255, 255,   0],
                           [  0, 255,   0],
                           [  0, 255,   0],
                           [  0, 255,   0],
                           [  0, 255,   0],
                           [  0, 255,   0],
                           [255, 255, 255]],

                    '2':[   [  0, 255, 255, 255,   0],
                        [255,   0,   0,   0, 255],
                        [  0,   0,   0,   0, 255],
                        [  0,   0,   0, 255,   0],
                        [  0,   0, 255,   0,   0],
                        [  0, 255,   0,   0,   0],
                        [255,   0,   0,   0,   0],
                        [255, 255, 255, 255, 255]],

                    '3':[[0, 255, 255,   0],
                         [255,   0,   0, 255],
                         [  0,   0,   0, 255],
                         [  0, 255, 255,   0],
                         [  0,   0,   0, 255],
                         [  0,   0,   0, 255],
                         [255,   0,   0, 255],
                         [  0, 255, 255,   0]],

                    '4':[ [255,   0,   0,   0],
                           [255,   0,   0,   0],
                           [255,   0,   0,   0],
                           [255,   0, 255,   0],
                           [255,   0, 255,   0],
                           [255, 255, 255, 255],
                           [  0,   0, 255,   0],
                           [  0,   0, 255,   0]],

                    '5':[  [255, 255, 255, 255],
                           [255,   0,   0,   0],
                           [255,   0,   0,   0],
                           [255, 255, 255,   0],
                           [  0,   0,   0, 255],
                           [  0,   0,   0, 255],
                           [255,   0,   0, 255],
                           [  0, 255, 255,   0]],

                    '6':[[  0,   0, 255, 255,   0],
                           [  0, 255,   0,   0, 255],
                           [255,   0,   0,   0,   0],
                           [255,   0, 255, 255,   0],
                           [255, 255,   0,   0, 255],
                           [255,   0,   0,   0, 255],
                           [255,   0,   0,   0, 255],
                           [  0, 255, 255, 255,   0]],

                    '7':[[255, 255, 255, 255],
                           [  0,   0,   0, 255],
                           [  0,   0, 255,   0],
                           [  0,   0, 255,   0],
                           [  0, 255,   0,   0],
                           [  0, 255,   0,   0],
                           [255,   0,   0,   0],
                           [255,   0,   0,   0]],

                    '8':[[  0, 255, 255, 255,   0],
                           [255,   0,   0,   0, 255],
                           [255,   0,   0,   0, 255],
                           [  0, 255, 255, 255,   0],
                           [255,   0,   0,   0, 255],
                           [255,   0,   0,   0, 255],
                           [255,   0,   0,   0, 255],
                           [  0, 255, 255, 255,   0]],

                    '9':[[  0, 255, 255, 255,   0],
                           [255,   0,   0,   0, 255],
                           [255,   0,   0,   0, 255],
                           [  0, 255,   0,   0, 255],
                           [  0,   0, 255, 255, 255],
                           [  0,   0,   0,   0, 255],
                           [  0,   0,   0,   0, 255],
                           [  0,   0,   0,   0, 255]]}

        for i,ele in enumerate(digitroi.values()):
            # roi cannot be np array to compare
            if ele == roi.tolist():
                return i
        return -1
    def marginInvest(self):
        """ invest on top 1 of 3 item from self.item_stat.
            assumes self.item_stat is a populated """

        items = []
        updated_margins = self.item_stat.copy()

        for i in range(1):
            for itemname,stats in updated_margins.items():
                highest_roi = max([self.item_stat[itemname]['roi'] for itemname in self.item_stat.keys()])
                if highest_roi == stats['roi']:
                    items.append(itemname)
                    updated_margins.pop(itemname)
                    break
        # display top 3 items to invest
        # print(items)
        # for item in items:
        #     self.getMargin(item)
        # buy X amnt of items at low based on roi weight
        total_roi = sum([self.item_stat[itemname]['roi'] for itemname in items])
        if self.cash == 0:
            self._setCash()
        # buy list, contains itemname qty and buying price
        buying_list = {}
        for itemname in items:
            weight = self.item_stat[itemname]['roi']/total_roi
            low = self.item_stat[itemname]['low']
            high = self.item_stat[itemname]['high']
            margin = self.item_stat[itemname]['margin']
            qty = (weight * self.cash)//low
            print(f"\n{itemname.upper()}\nBUY: {qty:.0f} @{low}gc:")
            print(f"SELL: @{high}gc")
            print(f"PROFIT: {margin*qty}gc")
            buying_list[itemname] = (qty,low,margin)
        # start buying x amount based on weight
        for itemname in buying_list.keys():
            if margin == 1:
                continue
            qty = buying_list[itemname][0]
            price = buying_list[itemname][1]
            margin = buying_list[itemname][2]

            self.buySellItem('buy',itemname,qty=qty,price=price)
if __name__ == "__main__":
    Trade = GE_Trading(0)
    Trade.set_main_wndw()

    # print(Trade.item_stat)
    while True:
        Trade.collMargins(items)
        Trade.marginInvest()
        input("Press ENTER for another investment")
