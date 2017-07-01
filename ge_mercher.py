from modules import Screenshot
import pyautogui
import cv2
import numpy as np


def main():
    # gets screen size
    w, h = pyautogui.size()
    # takes screen screenshot. Returns  hsv format image
    scrn_scrnshot = Screenshot.this(0, 0, w, h, 'hsv')
    #cv2.imshow('img', scrn_scrnshot)
    # cv2.waitKey(0)

    # find Grand exchange window
    lower_hsv = np.array([12, 0, 7])
    upper_hsv = np.array([40, 62, 64])
    # mask of applied values
    mask = cv2.inRange(scrn_scrnshot, lower_hsv, upper_hsv)
    cv2.imshow('img', mask)
    cv2.waitKey(0)
    return

    # find contours to get sides of rectangle
    _, contours, h = cv2.findContours(mask, 1, 2)

    for cnt in contours:
        # looks for biggest square
        # if cv2.contourArea(cnt) <= 1695.0:
        #    continue
        # checks contour sides
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        # Square found here vvvv
        if len(approx) == 4:
            #print("square of {}".format(cv2.contourArea(cnt)))
            # cv2.drawContours(rs_window,[cnt],0,(255,255,255),-1)

            # get geometry of approx
            # add rs coords
            x, y, w, h = cv2.boundingRect(cnt)
            print(cv2.contourArea(cnt))


main()
