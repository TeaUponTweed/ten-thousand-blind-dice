import sys

import cv2
import numpy as np

if __name__ == '__main__':
    assert len(sys.argv) > 1
    img = cv2.imread(sys.argv[1])
    img = cv2.resize(img,(400,500))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,gray = cv2.threshold(gray,127,255,0)
    gray2 = gray.copy()
    mask = np.zeros(gray.shape,np.uint8)
    contours, hier = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if 200<cv2.contourArea(cnt)<5000:
            cv2.drawContours(img,[cnt],0,(0,255,0),2)
            cv2.drawContours(mask,[cnt],0,255,-1)
