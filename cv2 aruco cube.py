import math
import numpy as np
import cv2
import random
from cv2 import aruco

'''functions:'''
def nothing(x):
   pass
'''variables:'''


'''cv setup:'''
frame_height = 640
frame_width = 640
frame = np.zeros(shape=(frame_height, frame_width, 3), dtype=np.uint8)
font = cv2.FONT_HERSHEY_TRIPLEX
center = (frame_width/2, frame_height/2, 0)
video = cv2.VideoCapture(0)

#cv2.createTrackbar('rotation about x', 'frame', 360, frame_width, nothing)
'''oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'''


'''oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'''



'''while loop'''
while(1):
    #angle_x = cv2.getTrackbarPos("rotation about x", "frame")

    check, frame = video.read()

    cv2.imshow('original', frame)
    key_value = cv2.waitKey(30)
    if key_value == ord('q'):
        break
