import cv2
import numpy as np
import math as m
import time
from cv2 import aruco
import cv2, PIL
from ar_markers import detect_markers
import random

##########  SETUP VAR  ##########
feed_from_website = False
is_flooded = False

statuses_of_balls = []
##########  FUNCTIONS  ##########
def nothing(x):
    pass

def isUpright(corners):
    bottom_left = corners[0] 
    top_left = corners[1]
    top_right = corners[2]
    bottom_right = corners[3]

    if bottom_left[1] < top_right[1]:
        is_wrong = True
    elif bottom_right[1] < top_left[1]:
        is_wrong = True
    
    else:
        is_wrong = False

    return is_wrong

def id_number(contour_local_x_value):
    M = cv2.moments(contour_local_x_value)
    id_number = int(M['m10'] / M['m00'])
    # print (x_value)
    return id_number

##########  VARIABLES  ##########
blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)
cyan = (255, 255, 0)
yellow = (0, 255, 255)
magenta = (255, 0, 255)
colors = [blue, green, red, cyan, yellow, magenta]

height_of_frame = 480
width_of_frame = 640

capture = cv2.VideoCapture(0)
if capture.isOpened():  # try to get the first frame
    frame_captured, frame = capture.read()
else:
    frame_captured = False

########## WHILE LOOP  ##########
while(1):

    #gets raw camera feed, makes gray image and displays both

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
    parameters =  aruco.DetectorParameters_create()

    corners, ids, rejected_img_points = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    gray = aruco.drawDetectedMarkers(frame, corners)
    
    try: 
        number_of_markers = len(ids)
        print(number_of_markers)
    except:
        print("no available markers")
        number_of_markers = None

    if number_of_markers is not None:

        statuses_of_balls = [] 
        while len(statuses_of_balls) < number_of_markers:
            statuses_of_balls.append(0)
        for i in range(number_of_markers):
            color = yellow
            this_id = ids[i][0]
            this_corner = corners[i][0][1]
            cv2.putText(frame, "ID #" + str(this_id), (this_corner[0], this_corner[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)


            these_corners = corners[i][0]
            is_wrong = isUpright(these_corners)

            statuses_of_balls[i] = is_wrong
        
        print(ids)
        print(statuses_of_balls)




    cv2.imshow('markers', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'): #q to quit
        break
    frame_captured, frame = capture.read()