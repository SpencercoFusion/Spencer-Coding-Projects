import cv2
import numpy as np
import math as m
import urllib.request
from PIL import Image
import time
import argparse
import time

def on_trackbar(val):
    alpha = val / alpha_slider_max
    beta = ( 1.0 - alpha )
    dst = cv.addWeighted(src1, alpha, src2, beta, 0.0)
    cv.imshow(title_window, dst)

def nothing(x):
    pass

def getImage(url):
    with urllib.request.urlopen(url) as url:
        with open('temp.jpg', 'wb') as f:
            f.write(url.read())
    image = Image.open('temp.jpg')
    image = np.array(image)
    #image = (image/256).astype('uint8')
    return image

def get_contour_center(contour_local_for_center):
    M = cv2.moments(contour_local_for_center)
    center_x = int(M['m10'] / M['m00'])
    center_y = int(M['m01'] / M['m00'])

    return center_x, center_y

movement_detected = False
get_calibration_centers = True
cv2.namedWindow('mask')
cv2.createTrackbar('hue_l', 'mask', 0, 180, on_trackbar)
cv2.createTrackbar('hue_u', 'mask', 180, 180, on_trackbar)
cv2.createTrackbar('sat_l', 'mask', 0, 255, on_trackbar)
cv2.createTrackbar('sat_u', 'mask', 255, 255, on_trackbar)
cv2.createTrackbar('val_l', 'mask', 140, 255, on_trackbar)
cv2.createTrackbar('val_u', 'mask', 255, 255, on_trackbar)

url = 'http://192.168.86.26/picture/1/current/'


pure_image = getImage(url)
frame_height = len(pure_image)
frame_width = len(pure_image[0])
print(str(frame_width), ', ', str(frame_height))
previous_time = time.time()
while (1):
    movement_detected = False
    hue_l = cv2.getTrackbarPos('hue_l', 'mask')
    hue_u = cv2.getTrackbarPos('hue_u', 'mask')
    sat_l = cv2.getTrackbarPos('sat_l', 'mask')
    sat_u = cv2.getTrackbarPos('sat_u', 'mask')
    val_l = cv2.getTrackbarPos('val_l', 'mask')
    val_u = cv2.getTrackbarPos('val_u', 'mask')
    
    if time.time() > (5 + previous_time):
        pure_image = getImage(url)
        previous_time = time.time()
        #print("CHANGING IMAGEE!!")
        print('movement', ('is') if movement_detected else ('not'), 'detected')

    image = pure_image
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #cv2.drawContours(gray, )
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    lower_green = np.array([hue_l, sat_l, val_l])
    upper_green = np.array([hue_u, sat_u, val_u])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    result = cv2.bitwise_and(image, image, mask=mask)
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=3)
    dilation = cv2.dilate(erosion, kernel, iterations=3)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(rgb, contours, -1, (255, 0, 0), 3)
    


    if len(contours) is not 2:
        movement_detected = True
    else:
        ball_1_center = get_contour_center(contours[0])
        ball_2_center = get_contour_center(contours[1])
        #print(ball_1_center,'  ', ball_2_center)

    '''
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 1, 
                  param1 = 100,
                  param2 = upper_val,
                  minRadius = 25,
                  maxRadius = 100)
    if circles is not None:
        for i in circles[0,:]:
            cv2.circle(gray,(i[0],i[1]),i[2],(0,255,0),2)
            cv2.circle(gray,(i[0],i[1]),2,(0,0,255),3)

        cv2.imshow('circles', gray)
    print(circles)   
    '''
    cv2.imshow('dilation', dilation)
    cv2.imshow('image', image)
    cv2.imshow('gray', gray)
    cv2.imshow('rgb', rgb)
    cv2.imshow('mask', mask)

    if get_calibration_centers:
        circle_1_default = ball_1_center
        circle_2_default = ball_2_center
        get_calibration_centers = False
    
    if ball_1_center[0] > (circle_1_default[0] + 10) or ball_1_center[0] < (circle_1_default[0] - 10):
        movement_detected = True
    if ball_1_center[1] > (circle_1_default[1] + 10) or ball_1_center[1] < (circle_1_default[1] - 10):
        movement_detected = True
    if ball_2_center[0] > (circle_2_default[0] + 10) or ball_2_center[0] < (circle_2_default[0] - 10):
        movement_detected = True    
    if ball_2_center[1] > (circle_2_default[1] + 10) or ball_2_center[1] < (circle_2_default[1] - 10):
        movement_detected = True    
    
    cv2.putText(image, ('Movement') if movement_detected else ('No Movement'), (20, frame_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255) if movement_detected else (255, 0, 0), 2)

    key_value = cv2.waitKey(30)
    if key_value == ord('q'):
        break
    

'''
while 1:
    io.imshow(io.imread(url))
    io.show()
'''