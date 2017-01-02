import cv2
import numpy as np
#from modules import Screenshot
from modules import RS
from modules import Mouse


play_img,psx,psy = RS.getPlayingScreen()

lower_gray = np.array([0,0,153])
upper_gray = np.array([8,25,209])

mines = {
    0: (np.array([0,0,153]), np.array([8,25,209])),
    1: (np.array([0,0,72]), np.array([2,25,144]))
}

for mine_key  in mines.keys():
    print("Mine: {}".format(mine_key))
    lower = mines[mine_key][0]
    upper = mines[mine_key][1]

    mask = cv2.inRange(play_img, lower, upper)

    kernel = np.ones((10,10), np.uint8)

    closing  =  cv2.morphologyEx(mask.copy(), cv2.MORPH_CLOSE, kernel)


    cv2.imshow('mask', mask)
    cv2.imshow('closing', closing)
    cv2.waitKey(0)

    _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for con in contours:
        M = cv2.moments(con)
        if cv2.contourArea(con) > 20:
            # Shows the mask

            #centroid from img moments
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            #combine psx,psy coords with centroid coords from above
            cx += psx
            cy += psy

            print("Area:",cv2.contourArea(con))
            print(con[0][0][0],con[0][0][1])
            #Mouse.moveTo(cx,cy)
        else:
            continue

