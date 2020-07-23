import math
import numpy as np
import cv2 as cv2
from cv2 import cv2
im = cv2.imread('500%_doubleTall_@.PNG')
inverted = cv2.bitwise_not(im)
get_arr_sum = lambda image: int(np.sum(image) / (len(im) * len(im[0]) * len(im[0, 0])))
total = get_arr_sum(im)
inv_total = get_arr_sum(inverted)
print(total)
print(inv_total)
while(1):
    cv2.imshow('im', im)
    cv2.imshow('inverted', inverted)
    k = cv2.waitKey(20)
    if k == ord('q'):
        break