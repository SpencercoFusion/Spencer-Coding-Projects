import math
import numpy as np
import cv2
import random

'''functions:'''
def nothing(x):
   pass

def distance(p1, p2): # give two, two dimensional points
    print(p1)
    print(p2)
    x1, y1 = p1
    x2, y2 = p2

    d_x = x1 - x2
    d_y = y1 - y2
 
    distance = math.sqrt((d_x)**2 + (d_y)**2)
    return distance

def true_distance(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    d_x = x1 - x2
    d_y = y1 - y2
    d_z = z1 - z2
    
    distance = math.sqrt((d_x)**2 + (d_y)**2 + (d_z)**2)
    return distance

def apply_rotation_z(point, point_of_rotation, deg_z):
    radius = distance((point[0], point[1]), (point_of_rotation[0], point_of_rotation[1]))
    #print(radius)
    x = point[0] - center[0]
    y = point[1] - center[1]
    z = point[2]

    original_angle = math.atan(y/x) * (180/math.pi)
   
    if ((x < 0)):
        original_angle = original_angle - 180
    
    target_angle = original_angle + deg_z

    x = radius * math.cos( (target_angle * math.pi) / 180)
    y = radius * math.sin( (target_angle * math.pi) / 180)

    x = x + center[0]
    y = y + center[1]

    #print(distance(point, center))
    return [x, y, z]

def apply_rotation_x(point, point_of_rotation, deg_x):
    radius = distance((point[1], point[2]), (point_of_rotation[1], point_of_rotation[2]))
    #print(radius)
    x = point[0] - center[0]
    y = point[1] - center[1]
    z = point[2]

    try:
        original_angle = math.atan(z/y) * (180/math.pi)
    except:
        print("error")
    if ((y < 0)):
        original_angle = original_angle - 180
    
    target_angle = original_angle + deg_x

    y = radius * math.cos( (target_angle * math.pi) / 180)
    z = radius * math.sin( (target_angle * math.pi) / 180)

    x = x + center[0]
    y = y + center[1]

    #print(distance(point, center))
    return [x, y, z]

def apply_rotation_y(point, point_of_rotation, deg_y):
    radius = distance((point[0], point[2]), (point_of_rotation[0], point_of_rotation[2]))
    #print(radius)
    x = point[0] - center[0]
    y = point[1] - center[1]
    z = point[2]

    original_angle = math.atan(x/z) * (180/math.pi)
   
    if ((z < 0)):
        original_angle = original_angle - 180
    
    target_angle = original_angle + deg_y

    z = radius * math.cos( (target_angle * math.pi) / 180)
    x = radius * math.sin( (target_angle * math.pi) / 180)

    x = x + center[0]
    y = y + center[1]

    #print(distance(point, center))
    return [x, y, z]  

'''variables:'''

side_length = 300

'''cv setup:'''

frame_height = 640
frame_width = 640
cv2.namedWindow('frame')
frame = np.zeros(shape=(frame_height, frame_width, 3), dtype=np.uint8)
font = cv2.FONT_HERSHEY_TRIPLEX
center = (frame_width/2, frame_height/2, 0)

cv2.createTrackbar('rotation about x', 'frame', 360, frame_width, nothing)
cv2.createTrackbar('rotation about y', 'frame', 360, frame_height, nothing)
cv2.createTrackbar('rotation about z', 'frame', 360, frame_width, nothing)

'''oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'''


[   [x1, y1, z1],
    [x2, y2, z2],
    [x3, y3, z3],
    [x4, y4, z4],
    [x5, y5, z5],
    [x6, y6, z6],
    [x7, y7, z7],
    [x8, y8, z8]    ]=[ [-1, -1, -1], #1
                        [1, -1, -1],  #2
                        [-1, 1, -1], #3
                        [1, 1, -1],  #4
                        [-1, -1, 1], #5
                        [1, -1, 1],  #6
                        [-1, 1, 1], #7
                        [1, 1, 1] ] #8

p1 = [x1, y1, z1]
p2 = [x2, y2, z2]
p3 = [x3, y3, z3]
p4 = [x4, y4, z4]
p5 = [x5, y5, z5]
p6 = [x6, y6, z6]
p7 = [x7, y7, z7]
p8 = [x8, y8, z8]

points = [p1, p2, p3, p4, p5, p6, p7, p8]

for i in range(len(points)):
    point = points[i]
    point[0] = (point[0] * side_length/2) + center[0]
    point[1] = (point[1] * side_length/2) + center[1]
    point[2] = point[2] * side_length/2
'''oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'''

previous_angle_x = 0
previous_angle_y = 0
previous_angle_z = 0

'''while loop'''

while(1):
    angle_x = cv2.getTrackbarPos("rotation about x", "frame")
    angle_y = cv2.getTrackbarPos("rotation about y", "frame")
    angle_z = cv2.getTrackbarPos("rotation about z", "frame")

    if (previous_angle_z != angle_z):
        for i in range(len(points)):
            points[i] = apply_rotation_z(points[i], center, (angle_z - previous_angle_z))
    
    if (previous_angle_x != angle_x):
        for i in range(len(points)):
            points[i] = apply_rotation_x(points[i], center, (angle_x - previous_angle_x))
    
    if (previous_angle_y != angle_y):
        for i in range(len(points)):
            points[i] = apply_rotation_y(points[i], center, (angle_y - previous_angle_y))


    cv2.rectangle(frame, (0,0), (frame_height, frame_width), (255, 255, 255), -1)
    #print(center)
    for i in range(len(points)):
        this_point = points[i]
        '''
        px = int((this_point[0] * side_length/2) + center[0])
        py = int((this_point[1] * side_length/2) + center[1])
        pz = int((this_point[2] * side_length/2))
        '''
        px = this_point[0]
        py = this_point[1]
        pz = this_point[2]

        cv2.circle(frame, (int(px), int(py)), 2, (255, 0, 0), -1)
        cv2.putText(frame, str(i), (int(this_point[0]), int(this_point[1])), font,  0.5, (255, 0, 0), 1)
        for t in range(len(points)):
            second_point = points[t]
            if (true_distance(this_point, second_point) < side_length + 1) & (true_distance(this_point, second_point) > side_length - 1):
                #print("yes")
                cv2.line(frame, (int(this_point[0]), int(this_point[1])), (int(second_point[0]), int(second_point[1])), (0, 0, 0))
            else:
                #print("no, because distance = " + str(true_distance(this_point, points[t])))
                nothing
    
    



        

    previous_angle_x = angle_x
    previous_angle_y = angle_y
    previous_angle_z = angle_z

    cv2.imshow('original', frame)
    key_value = cv2.waitKey(30)
    if key_value == ord('q'):
        break
