import cv2 
from cv2 import cv2
import numpy as np 
import math as m 
import random 
import matplotlib.pyplot as plt

def nothing(x):
    pass
def getPixelMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('BGR: ' + str(backyard_1[y, x]))
        print('HSV: ' + str(bgr2hsv(backyard_1[y, x])))
        print('')
def hsv2bgr(h_s_v):

    #bgr_red = np.uint8([[[0, 0, 255]]])
    #hsv_red = cv2.cvtColor(bgr_red, cv2.COLOR_BGR2HSV)

    hsv_space = np.uint8([[h_s_v]])
    bgr_space = cv2.cvtColor(hsv_space, cv2.COLOR_HSV2BGR)
    b = int(bgr_space[0, 0, 0])
    g = int(bgr_space[0, 0, 1])
    r = int(bgr_space[0, 0, 2])
    return (b, g, r)
def bgr2hsv(b_g_r):

    #bgr_red = np.uint8([[[0, 0, 255]]])
    #hsv_red = cv2.cvtColor(bgr_red, cv2.COLOR_BGR2HSV)

    bgr_space = np.uint8([[b_g_r]])
    hsv_space = cv2.cvtColor(bgr_space, cv2.COLOR_BGR2HSV)
    h = int(hsv_space[0, 0, 0])
    s = int(hsv_space[0, 0, 1])
    v = int(hsv_space[0, 0, 2])
    return (h, s, v)
cv2.namedWindow('vars')
cv2.namedWindow('backyard_1')
cv2.setMouseCallback('backyard_1', getPixelMouse)
cv2.createTrackbar('brightness', 'vars', 0, 255, nothing)
brightness_range = 10

scale_factor = 0.3
im_path = r'C:\Users\spenc\Downloads\backgroundim1.jpg'
backyard_1 = cv2.imread(im_path)
print(backyard_1.shape)
backyard_1 = cv2.resize(backyard_1, (int(backyard_1.shape[1] * scale_factor), int(backyard_1.shape[0] * scale_factor))            )
hsv_by1 = cv2.cvtColor(backyard_1, cv2.COLOR_BGR2HSV)
value = backyard_1[:, :, 2]


values_only = np.resize(hsv_by1[:, :, 2], (len(hsv_by1) * len(hsv_by1[0])))
num_bins = 50
n, bins, patches = plt.hist(values_only, num_bins, facecolor='blue', alpha=0.5)
#plt.show()


while(1):
    colored = hsv_by1.copy()
    min_bright = cv2.getTrackbarPos('brightness', 'vars') - brightness_range
    max_bright = cv2.getTrackbarPos('brightness', 'vars') + brightness_range
    min_bright = 0 if min_bright < 0 else min_bright
    max_bright = 255 if max_bright > 255 else max_bright
    h = colored[:, :, 0]
    s = colored[:, :, 1]
    v = colored[:, :, 2]
    truth_arr = np.full((colored.shape[0], colored.shape[1]), 0, dtype=np.uint8)
    truth_arr[:, :] = (v[:, :] < max_bright) * (v[:, :] > min_bright) * 255 #+ (h[:, :] > max_bright) + (h[:, :] < min_bright)

    anti_truth = cv2.bitwise_not(truth_arr)
    pixel_if_in_range = colored.copy()
    pixel_if_in_range[:, :, 0] = 180
    pixel_if_in_range[:, :, 1] = 255
    pixel_if_in_range[:, :, 2] = colored[:, :, 2]
    default_pixels = cv2.bitwise_and(colored, colored, mask=anti_truth)
    pixels_in_range = cv2.bitwise_and(pixel_if_in_range, pixel_if_in_range, mask=truth_arr)

    colored = cv2.bitwise_or(pixels_in_range, default_pixels)
    colored[:, :, 1] = 255
    colored = cv2.cvtColor(colored, cv2.COLOR_HSV2BGR)

    
    cv2.imshow('backyard_1', backyard_1)
    cv2.imshow('value', value)
    cv2.imshow('colored', colored)
    k = cv2.waitKey(20)
    if k == ord('q'):
        break