import sys

import cv2
import numpy as np

if __name__ == '__main__':
    assert len(sys.argv) > 1
    img = cv2.imread(sys.argv[1])
    img = cv2.resize(img,(400,500))
    print(img.shape)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    (_,a),(_,b),(_,c) = cv2.threshold(img[:, :, 0],127,255,0), cv2.threshold(img[:, :, 1],127,255,0), cv2.threshold(img[:, :, 2],127,255,0)
    gray = a & b & c
    mask = np.zeros(gray.shape,np.uint8)
    # print(mask)
    contours, hier = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    def gen_contours(): 
        for cnt in contours:
            yield cv2.contourArea(cnt), cnt
    _, cnt = max(gen_contours(), key=lambda x: x[0])
    (x1, y1), (x2, y2), _ = cv2.fitEllipse(cnt)
    print (x2-x1)/(y2-y1)

    cv2.drawContours(img,[cnt],0,(0,255,0),2)
    cv2.drawContours(mask,[cnt],0,255,-1)

    # cv2.bitwise_not(gray2,gray2,mask)
    cv2.imshow('IMG',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()