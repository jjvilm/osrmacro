import cv2
import numpy as np
#from modules import Screenshot
from modules import RS
from modules import Mouse
from modules import RandTime
from modules import Screenshot

def find_motherload_mine():
    """Returns mine's location x, and y coords"""
    play_img,psx,psy = RS.getPlayingScreen()


    mines = {
        0: (np.array([0,0,153]), np.array([8,25,209])),
        1: (np.array([0,0,72]), np.array([2,25,144]))
    }

    for mine_key  in mines.keys():
        #print("Mine: {}".format(mine_key))
        lower = mines[mine_key][0]
        upper = mines[mine_key][1]

        mask = cv2.inRange(play_img, lower, upper)

        kernel = np.ones((10,10), np.uint8)

        closing  =  cv2.morphologyEx(mask.copy(), cv2.MORPH_CLOSE, kernel)


        #cv2.imshow('mask', mask)
        #cv2.imshow('closing', closing)
        #cv2.waitKey(0)

        _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours[0].any():
            pass
        else:
            print('didnt find contours')
            break

        for con in contours[::-1]:
            M = cv2.moments(con)
            if cv2.contourArea(con) > 20:
                # Shows the mask

                #centroid from img moments
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])

                #combine psx,psy coords with centroid coords from above
                cx += psx
                cy += psy

                #print("Area:",cv2.contourArea(con))
                #print(con[0][0][0],con[0][0][1])
                Mouse.moveClick(cx,cy, 1)
                return cx,cy
            else:
                continue

def check_mine_availability(mine_x, mine_y):
    RandTime.randTime(3,0,0,5,9,9)
    cmx, cmy = Mouse.mouse_loc()
    mine_x = cmx - mine_x
    mine_y = cmy - mine_y
    while 1:
        # expands by 4X4 to check color values
        x = mine_x - 2
        y = mine_y - 2
        x2 =mine_x + 2
        y2 =mine_y + 2

        checked_area  = Screenshot.shoot(x,y,x2,y2, 'hsv')

        lower_gray = np.array([0,0,153])
        upper_gray = np.array([8,25,209])

        mask = cv2.inRange(checked_area, lower_gray, upper_gray)
        for colors in mask:
            for value in colors:
                if value == 255:
                    print('mine ACTIVE')
                    RandTime.randTime(5,0,0,5,9,9)
                    break
        else:
            print("mine INACTIVE")
            break

        #cv2.imshow('mask', mask)
        #cv2.waitKey(0)

def main():
    # runs main loop
    # gets initial count of inventory items
    item_n = RS.inventory_counter()
    while 1:
        # stops when inventory is full
        if item_n == 28:
            RS.play_sound()
            break
        try:
        # keeps mining
            cx, cy, = find_motherload_mine()
            #check_mine_availability(cx,cy)

        except:
        # slows down the loop by ~second
            RandTime.randTime(1,0,0,1,9,9)
            continue
        # waits for obtained ore to restart loop
        item_n = RS.inventory_counter()

        times_till_break = 0
        while 1:
            # safety measure to make sure it does not get stuck counting inventory
            if times_till_break == 3:
                print('Escaping inventory loop')
                times_till_break = 0
                break
            current_n_items = RS.inventory_counter()
            # counts to make sure +1 has been added to inv
            if current_n_items >= item_n + 1:
                item_n = current_n_items
                RandTime.randTime(4,0,0,7,9,9)
                break
            else:
                times_till_break += 1
                RandTime.randTime(7,0,0,15,9,9)
                continue
main()
