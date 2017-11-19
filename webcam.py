#pyserial
import serial
import random
from collections import OrderedDict
import time
import glob

import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

from calc_white_area import get_white_area

def get_middle_square(img, frac):
    rows, cols, _ = frame.shape
    side_length = int(max(frac*rows, frac*cols))
    # print(rows, cols, side_length)
    assert side_length < rows and side_length < cols
    col_offset = (cols - side_length)//2
    row_offset = (rows - side_length)//2
    # print(col_offset)
    # print(row_offset)
    return img[row_offset:row_offset+side_length, col_offset:col_offset+side_length,  :]

if __name__ == '__main__':
    max_saved_frame = -1
    try:
        # hl, = plt.plot([], [])
        # plt.ion()
        cap = cv2.VideoCapture(0)
        # data = OrderedDict()
        # frames = OrderedDict()
        frameid = 0

        serial_name = glob.glob('/dev/tty.usbserial*')
        ser = serial.Serial(serial_name[0], 9600)
        def go(speed=192, sleep=1):
            print('go')
            ser.write(str(speed))
            time.sleep(sleep)

        def stop():
            print('stop')
            ser.write('0')
            time.sleep(1)

        def roll():
            print('rolling')
            go(170, .9)
            # for _ in range(random.randint(2, 4)):
            #     speed = random.randint(1, 170)
            #     go(str(speed), random.random())

        time.sleep(1)
        stop()
        roll()
        # go()

        while True:
            ret, frame = cap.read()
            frameid += 1
            # print(frame.shape)
            # frame = frame[rows//3:2*rows//3, cols//3:2*cols//3, :]
            # print(frame.shape)
            frame = get_middle_square(frame, .5)
            try:
                area, cnt = get_white_area(frame)
            except ValueError:
                pass
            else:
                # data[frameid] = area
                # frames[frameid] = frame
                # if len(data) > 10:
                #     data.popitem(last=False)
                #     frames.popitem(last=False)
                # plt.clf()
                # x, y = map(np.array, zip(*data.items()))
                # plt.plot(x, y)
                # local_maxima_indexes, = argrelextrema(y, np.greater)
                # ix = np.argmax(y)
                # maximizing_frame_id = x[ix]
                # for ix in local_maxima_indexes:
                    # print(ix)
                cv2.drawContours(frame,[cnt],0,(0,255,0),2)
                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # print(area)
                if area > 8000:
                    # plt.axvline(x=maximizing_frame_id)
                    # if maximizing_frame_id < frameid and maximizing_frame_id > max_saved_frame:
                    stop()
                    # time.sleep(1)
                    ret, frame = cap.read()
                    frame = get_middle_square(frame, .5)
                    cv2.imwrite('/Volumes/dataPit/rolling_images/{}.png'.format(frameid), frame)

                    # max_saved_frame = maximizing_frame_id
                    roll()
                    # stop()
                    go()

                # plt.show()
                # plt.pause(0.001)
                

            # cv2.imshow('frame',frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

    finally:
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
