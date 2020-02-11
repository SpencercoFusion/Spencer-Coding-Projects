import math
import numpy as np
import cv2
import random

'oO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0Oo'
'''
   triangles =[
   [
   [[v1,    v2,     v3  ],
   [L1_2,  L2_3,   L3_1],
   [T1,    T2,     T3  ],
   [Cx,    Cy,     Cr  ],
   [Tp1,   Tp2,    Tp3 ]
   ]]
   ]  
'''
def nothing(x):
   pass

def getVal(value, set_num, triangle_num):
   if str(value) == 'v1':
       return triangles[set_num][triangle_num][0][0]
   if str(value) == 'v2':
       return triangles[set_num][triangle_num][0][1]
   if str(value) == 'v3':
       return triangles[set_num][triangle_num][0][2]

   if str(value) == 'L1_2':
       return triangles[set_num][triangle_num][1][0]
   if str(value) == 'L2_3':
       return triangles[set_num][triangle_num][1][1]
   if str(value) == 'L3_1':
       return triangles[set_num][triangle_num][1][2]

   if str(value) == 'T1':
       return triangles[set_num][triangle_num][2][0]
   if str(value) == 'T2':
       return triangles[set_num][triangle_num][2][1]
   if str(value) == 'T3':
       return triangles[set_num][triangle_num][2][2]

   if str(value) == 'Cx':
       return triangles[set_num][triangle_num][3][0]
   if str(value) == 'Cy':
       return triangles[set_num][triangle_num][3][1]
   if str(value) == 'Cr':
       return triangles[set_num][triangle_num][3][2]
  
   if str(value) == 'Tp1':
       return triangles[set_num][triangle_num][4][0]
   if str(value) == 'Tp1':
       return triangles[set_num][triangle_num][4][1]
   if str(value) == 'Tp1':
       return triangles[set_num][triangle_num][4][2]

def defineAngleOfPoints(p1, p2, p3):
    c = getDistance(p1, p2)
    b = getDistance(p3, p1)
    a = getDistance(p2, p3)
    height = math.sqrt(b**2 - (( (a**2) + (b**2) - (c**2)) **2) / (4 * a**2))
    t = (a**2 + b**2 - c**2) / (2 * a)
    k = (a**2 + c**2 - b**2) / (2 * a)

    if t <= 0:
        Angle_p1 = math.acos(height/c) - math.acos(height/b)
        Angle_p2 = math.asin(height/c)
        Angle_p3 = math.pi - math.asin(height/b)
        #print(' t <= 0 ')
    elif k <= 0:
        Angle_p1 = math.acos(height/b) - math.acos(height/c)
        Angle_p2 = math.pi - math.asin(height/c)
        Angle_p3 = math.asin(height/b)
        #print('k <= 0')
    else:   #k and t are both greater than 0
        Angle_p1 = (math.acos(height/b) + math.acos(height/c))
        Angle_p2 = math.asin(height/c)
        Angle_p3 = math.asin(height/b)
    
    Angle_p1 = 57.2958 * Angle_p1
    Angle_p2 = 57.2958 * Angle_p2
    Angle_p3 = 57.2958 * Angle_p3


    return Angle_p1, Angle_p2, Angle_p3


def getRadiusOfCircle(line1, center):
   radius_line = definePerpendicularLine(line1, center)
   poi = definePointOfIntersection(radius_line, lines[0])
   radius = getDistance(poi, center)
   return radius
def definePerpendicularLine(line1, p1):
   m = -1/(line1[0])
   b = p1[1] - m*p1[0]
   return(m, b)

def getDistance(p1, p2):
  
   x = p1[0] - p2[0]
   y = p1[1] - p2[1]
   distance = math.sqrt(x**2 + y**2)
   return distance

def defineCenterPoint(p1, p2):
   x = (p1[0] + p2[0]) / 2
   y = (p1[1] + p2[1]) / 2
   return(int(x),int(y))

def randomColor():
   blue = random.randint(0, 255)
   green = random.randint(0, 255)
   red = random.randint(0, 255)
   color = (blue, green, red)
   return color

def getB(m, p1):
   b = p1[1] - m * p1[0]
   return b

def defineLine(p1, p2):
   if (p1[0] - p2[0]) == 0:
       p1 = ((p1[0] + 1), p1[1])
   m = (p1[1] - p2[1]) / (p1[0] - p2[0])
   b = getB(m, p1)
   return (m, b, p1, p2)

def defineAngleBisector(line1, line2, opposite_line ):
   m =  math.tan( (math.atan(line1[0]) + math.atan(line2[0]))/2 )
   poi = definePointOfIntersection(line1, line2)

  
   if line1[2][0] < poi[0] < line2[3][0]:
       m = -1/m
   elif line1[2][0] > poi[0] > line2[3][0]:
       m = -1/m
   b = getB(m, poi)
   second_poi = definePointOfIntersection((m, b), opposite_line)
   return(m, b, poi, second_poi)

def definePointOfIntersection(line1, line2):

   if (line1[0] - line2[0]) == 0:
       line1 = (line1[0] + 0.001, line1[1])
   x = (line2[1] - line1[1]) / (line1[0] - line2[0])
   y = line1[0] * x + line1[1]
   point_of_intersection = (int(x), int(y))
   return(point_of_intersection)

'oO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0Oo'
vertices_colors = []
choose_new_colors = True

v1 = (253, 18)
v2 = (518, 400)
v3 = (221, 400)
vertices = [v1, v2, v3]

circles = []


frame_height = 640
frame_width = 640

font = cv2.FONT_HERSHEY_TRIPLEX
'oO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0Oo'
cv2.namedWindow('frame')
frame = np.zeros(shape=(frame_height, frame_width, 3), dtype=np.uint8)
cv2.createTrackbar('v1 x', 'frame', v1[0], frame_width, nothing)
cv2.createTrackbar('v1 y', 'frame', v1[1], frame_height, nothing)
cv2.createTrackbar('v2 x', 'frame', v2[0], frame_width, nothing)
cv2.createTrackbar('v2 y', 'frame', v2[1], frame_height, nothing)
cv2.createTrackbar('v3 x', 'frame', v3[0], frame_width, nothing)
cv2.createTrackbar('v3 y', 'frame', v3[1], frame_height, nothing)
cv2.createTrackbar('p x', 'frame', 350, frame_width, nothing)
cv2.createTrackbar('p y', 'frame', 250, frame_height, nothing)



'oO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0Oo'

while 1:
    v1 = (cv2.getTrackbarPos('v1 x', 'frame'), cv2.getTrackbarPos('v1 y', 'frame'))
    v2 = (cv2.getTrackbarPos('v2 x', 'frame'), cv2.getTrackbarPos('v2 y', 'frame'))
    v3 = (cv2.getTrackbarPos('v3 x', 'frame'), cv2.getTrackbarPos('v3 y', 'frame'))
    p = (cv2.getTrackbarPos('p x', 'frame'), cv2.getTrackbarPos('p y', 'frame'))
    
    if v1[0] == v2[0]:
        v2 = (v2[0] - 1, v2[1])
    if v1[0] == v3[0]:
        v3 = (v3[0] + 1, v3[1])
    if v3[0] == v2[0]:
        v2 = (v2[0] - 1, v2[1])
        
    if v1[1] == v2[1]:
        v2 = (v2[0], v2[1] - 1)
    if v1[1] == v3[1]:
        v3 = (v3[0], v3[1] + 1)
    if v3[1] == v2[1]:
        v2 = (v2[0], v2[1] - 1)
    vertices = [v1, v2, v3]

    cv2.rectangle(frame, (0,0), (frame_height, frame_width), (255, 255, 255), -1)
    ''''
    makes the equations of the lines that run through the
    points on the triangle v1 and v1: Lv1_v2 = [m, b]
    "m" describes slope
    "b" describes y-intercept
    '''
    L1_2 = defineLine(v1, v2)
    L2_3 = defineLine(v2, v3)
    L3_1 = defineLine(v3, v1)
    lines = [L1_2, L2_3, L3_1]
    '''
    makes the equations of the lines that are the
    angular bisector of each vertex v: Tv = [m, b, poi, second_poi]
    "m" describes slope
    "b" describes y-intercept
    "poi" describes point of intersection between angle bisector and two lines being bisected
    "second_poi" describes point of intersection of opposite side
    '''
    T1 = defineAngleBisector(L3_1, L1_2, L2_3, )
    T2 = defineAngleBisector(L1_2, L2_3, L3_1, )
    T3 = defineAngleBisector(L2_3, L3_1, L1_2, )
    angleBisectors = [T1, T2, T3]



    #cv2.line(frame, p, v1, (255,0,0), 2)

    #Lp_1 = getDistance(p, v1)
    Lp_2 = getDistance(p, v2)
    Lp_3 = getDistance(p, v3)
    p_sum = Lp_3**2 - Lp_2**2
    print(p_sum, Lp_3, Lp_2)

    for i in range(len(vertices)):
       cv2.circle(frame, vertices[i], 2, (0,0,0), -1)
       cv2.putText(frame, 'v' + str(i + 1), vertices[i], font,
                   0.5, (255,0,0), 1)


    for i in range(len(lines)):
       if (i + 1) >= len(lines):
           x = 0
       else:
           x = i + 1
       cv2.line(frame, vertices[i], vertices[x], (0,0,0), 2)
       cv2.putText(frame, str(round(lines[i][0], 2)),
                   defineCenterPoint(vertices[i],vertices[x]),
                   font, 0.5, (255, 0, 0), 1)


    for i in range(len(angleBisectors)):
        #center_point = defineCenterPoint(angleBisectors[])
        cv2.line(frame, angleBisectors[i][2], angleBisectors[i][3], (0,255,0), 1)


    Cx, Cy = definePointOfIntersection(angleBisectors[0], angleBisectors[1])
    center = (int(Cx), int(Cy))
    Cr = getRadiusOfCircle(lines[0], center)
    cv2.circle(frame, center, int(Cr), (255, 0, 0) )
    
    
    #print(L1_2, '   ', L2_3, '   ', L3_1)
    triangles =[
    [
    [[v1,    v2,     v3  ],
    [L1_2,  L2_3,   L3_1],
    [T1,    T2,     T3  ],
    [Cx,    Cy,     Cr  ],
    ]]
    ]  

    #print(print(defineAngleOfPoints(v1, v2, v3)))

    cv2.imshow('original', frame)
    key_value = cv2.waitKey(30)
    if key_value == ord('q'):
        break

'oO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0OoO0Oo'

cap.release()
cv2.destroyAllWindows()

