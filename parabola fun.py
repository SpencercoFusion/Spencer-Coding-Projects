import math
import numpy as np
import cv2
from cv2 import cv2
import random
import sys

'''functions:'''
def nothing(x):
   pass

def drawParabola():
    for x in range(frame_width * 2):
        fillPixel(x , parabola(x - frame_width / 2), (200, 200, 0))
    focus = (centerx, int(F))
    cv2.circle(frame, focus, 2, (100, 200, 0), -1)
    
    '''
    for x in range(frame_width):
        for y in range(frame_height):
            if (x * y) != 0:
                approx_normal_slope = -1/(2 * (1/k) * x) #this is the approximate slope of the normal line according to the parabola at x=x1
                a = 1
                b = (-k * approx_normal_slope)
                c = (-k * (approx_normal_slope * x + y))
                if (b**2 - (4 * a * c) > 0):
                    approx_x1 = (-b + math.sqrt(b**2 - (4 * a * c)))/(2 * a)     #these are x values on the parabola that intersect with the normal line
                    approx_x2 = (-b - math.sqrt(b**2 - (4 * a * c)))/(2 * a)
                    approx_y1 = parabola(approx_x1)
                    approx_y2 = parabola(approx_x2)
                    if distance(x, y, approx_x1, approx_y1) < line_thickness or distance(x, y, approx_x2, approx_y2) < line_thickness:
                        fillPixel(x + centerx, y + centerx, (230, 200, 0))
    '''

def drawRays():
    num_rays = 100
    global F
    for r in range(num_rays):
        t = r * 180/num_rays        #angle in degrees of original ray
        slope = math.tan(t * pi/180)
        if t >= 90:
            x_bound1 = k * (slope + math.sqrt((slope**2) - 4 * (-F/k))) / 2
        else:
            x_bound1 = k * (slope - math.sqrt((slope**2) - 4 * (-F/k))) / 2
        y_bound1 = parabola(x_bound1)
        if y_bound1 <= F:
            cv2.line(frame, (centerx, int(F)), (int(x_bound1 + centerx), int(y_bound1)), (0, 255, 255), 1)

            t_rad = t * pi/180   
            slope_of_tangent = tanLineSlope(x_bound1)
            angleTheta = math.atan(slope_of_tangent) - t_rad    #angle of incedence
            angleOfReflection = angleTheta + math.atan(slope_of_tangent)    #the angle that the reflected ray forms with the x-axis
            slopeOfReflection = math.tan(angleOfReflection)
            reflected_y_bound = frame_height
            if slopeOfReflection != 0:
                reflected_x_bound = (1/slopeOfReflection)*(reflected_y_bound - y_bound1) + x_bound1
                cv2.line(frame, (int(x_bound1 + centerx), int(y_bound1)), (int(reflected_x_bound) + centerx, reflected_y_bound), (0, 255, 200), 1)
            else:
                cv2.line(frame, (int(x_bound1 + centerx), int(y_bound1)), (int(x_bound1), reflected_y_bound), (0, 255, 200), 1)

def distance(x1, y1, x2, y2):
    return(math.sqrt((x1 - x2)**2 + (y1-y2)**2))

def parabola(x):
    return(x**2 * (1/k))

def tanLineSlope(x):
    return(((2/k)*x))

def fillPixel(x, y, color):
    if int(y) < frame_height and int(x) < frame_width:  
        frame[int(y), int(x)] = color
    #else:
        #print(str(x) + " or " + str(y) + " is out of bounds ")
'''variables:'''
k = 10**3
F = int(k/4)
pi = math.pi

line_thickness = 3
mm_per_side = 300
'''cv setup:'''
frame_height = 640
frame_width = 1200
cv2.namedWindow('frame')
frame = np.zeros(shape=(frame_height, frame_width, 3), dtype=np.uint8)
font = cv2.FONT_HERSHEY_TRIPLEX
centerx = int(frame_width/2)
centery = int(frame_height/2)

cv2.createTrackbar('k-val', 'frame', 100, 2800, nothing)
cv2.createTrackbar('F', 'frame', F, frame_height, nothing)
cv2.createTrackbar('scale', 'frame', 100, 100, nothing)

'''oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'''


'''oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'''



'''while loop'''
while(1):
    frame = np.zeros(shape=(frame_height, frame_width, 3), dtype=np.uint8)  
    k_val = cv2.getTrackbarPos("k-val", "frame")
    scale = cv2.getTrackbarPos("scale", "frame")
    F = cv2.getTrackbarPos("F", "frame")  * scale / 100 

    k = 1 + (k_val + 1) * scale / 100

    drawParabola()
    drawRays()
    cv2.imshow('original', frame)
    key_value = cv2.waitKey(30)
    if key_value == ord('q'):
        break
