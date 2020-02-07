import cv2 as cv2
from cv2 import cv2
import numpy as np
import math as m

frame_height = 1000
frame_width = 1000

number_of_points = 25
center = (frame_width/2, frame_height/2)
radius = 400

font = cv2.FONT_HERSHEY_SIMPLEX
green = (255, 0, 0)
blue = (0, 255, 0)
red = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

iterations = 0

number_of_rows = number_of_points - 1
path = r'C:\Users\spenc\Downloads\Anchor.png'   #image path
img = cv2.imread(path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

dictionary_of_pixels = {}
dictionary_of_strings = {}

def resizeImage(img_to_resize):
    img_height = len(img_to_resize)
    img_width = len(img_to_resize[0])
    resized_image = img_to_resize

    if img_height < frame_height:
        height_buffer = np.full(    ( int((frame_height - img_height)/2) , img_width), 255, dtype=np.uint8)
        resized_image = np.concatenate((height_buffer, img_to_resize, height_buffer), axis=0) 
        img_height = len(resized_image)
        #print("image height is " + str(img_height))
    img_height = len(resized_image)
    if img_width < frame_width:
        #print("this new image height is: " + str(img_height))
        width_buffer = np.full(     (img_height,  int((frame_width - img_width)/2) ), 255, dtype=np.uint8)
        #print(str(len(width_buffer)) + " is the height of buffer")
        #print(str(len(width_buffer[0])) + " is the length of buffer")

        resized_image = np.concatenate((width_buffer, resized_image, width_buffer), axis=1) 
    return(resized_image)    

def cutCircle(img_to_cut):    #crops image into circle, removes all points besides ones inside circle
    global radius           #radius of circle
    global frame_height, frame_width    #height and width of string img
    pixels_to_keep = []
    pixels_to_remove = []
    img_height = len(img_to_cut)  #width and height of image in pixels
    img_width = len(img_to_cut[0])
    this_center_x = img_width / 2
    this_center_y = img_height / 2
    for y in range(len(img_to_cut)):
        for x in range(len(img_to_cut[y])):
            if distance((x,y), (this_center_x, this_center_y)) < radius:
                pixels_to_keep.append((x,y))
            else:
                pixels_to_remove.append((x,y))
    return(pixels_to_keep, pixels_to_remove)

def blackOutPixels(these_pixels_to_remove, this_img):
    copy_of_image = this_img
    for p in these_pixels_to_remove:
        x, y = p
        if y < len(copy_of_image) and x < len(copy_of_image[0]):
            copy_of_image[y, x] = 0
    return copy_of_image

def invertThisImage(img_to_invert):
    t_inverted_img = (255 - img_to_invert)
    return t_inverted_img

def distance(p1, p2): #absolute distance between points p1 and p2
    x1, y1 = p1
    x2, y2 = p2
    distance = m.sqrt(  (x1-x2)**2  +   (y1-y2)**2  )
    return(distance)

def nextColor():
    global iterations
    bgr = hsv2bgr((100 / number_of_points * iterations, 180, 180))
    iterations = iterations + 1
    return bgr

def cvWindows():
    global frame 
    frame = np.zeros(shape=(frame_height, frame_width, 3), dtype=np.uint8)

def connectPoints(number_of_points):
    
    if number_of_points > 1:
        for i in range(number_of_points - 1):
           list_of_strings.append(makeString(number_of_points, i + 1, hsv2bgr((20 * i, 180, 180))))
        number_of_points = number_of_points - 1
        connectPoints(number_of_points)

def pixelsInaLine(this_string):

    l_m, l_b = stringToLine(this_string)
    #print("m and b are: " + str(l_m) +" "+ str(l_b))
    pixels_in_line = []
    if l_m is "vert":
        x = l_b
        for y in range(frame_height):
            if distance((x,y), center) <= radius:
                pixel = str((x,y))
                if pixel in dictionary_of_pixels.keys():
                    list_of_lines = dictionary_of_pixels[pixel]
                    list_of_lines.append(this_string)
                    dictionary_of_pixels[pixel] = list_of_lines
                else:
                    list_of_lines = [this_string]
                    dictionary_of_pixels[pixel] = list_of_lines
    else:
        for x in range(frame_width):
            y = int(l_m * x + l_b)
            if distance((x,y), center) <= radius:
                pixel = str((x, y))
                if pixel in dictionary_of_pixels.keys():
                    list_of_lines = dictionary_of_pixels[pixel]
                    list_of_lines.append(this_string)
                    dictionary_of_pixels[pixel] = list_of_lines
                    #print("adding line..." + pixel + " " + str(dictionary_of_pixels[pixel]))
                else:
                    list_of_lines = [this_string]
                    dictionary_of_pixels[pixel] = list_of_lines
    



def createIntersections(list_of_strings):
    #list_of_intersections = []
    pass
            

def makeString(id1, id2, color):
    p1 = pointToCoord(id1)
    p2 = pointToCoord(id2)
    cv2.line(frame, p1, p2, color, 1)
    if id1 < id2:
        t_string = (id1, id2)
    else:
        t_string = (id2, id1)
    return t_string



def intersection(string1, string2):
    m1, b1= stringToLine(string1)
    m2, b2= stringToLine(string2)
    if m1 != m2:
        if m1 == "vert":
            intersection_x = b1
            intersection_y = intersection_x * m2 + b2
        elif m2 == "vert":
            intersection_x = b2
            intersection_y = intersection_x * m1 + b1
        elif ((m1 - m2) != 0):
            intersection_x = (b2 - b1) / (m1 - m2)
            intersection_y = intersection_x * m1 + b1
    else: 
        intersection_x = 0
        intersection_y = 0
    return (int(intersection_x), int(intersection_y))

def stringToLine(string):
    x1, y1 = pointToCoord(string[0])
    x2, y2 = pointToCoord(string[1])
    if x1 != x2:
        m = (y1 - y2) / (x1 - x2)
        b = y1 - m * x1
    else:
        m = "vert"
        b = x1
    return(m, b)

def pointToCoord(pointID):
    global center
    center_x, center_y = center
    angle = pointID * 2 * m.pi / number_of_points
    point_x = int(m.cos(angle) * radius + center_x)
    point_y = int(m.sin(angle) * radius + center_y)
    cv2.circle(frame, (point_x, point_y), 1, white, -1)
    cv2.putText(frame, str(pointID), (point_x, point_y), font, 0.5, white)

    return(point_x, point_y)


def hsv2bgr(h_s_v):

    #bgr_red = np.uint8([[[0, 0, 255]]])
    #hsv_red = cv2.cvtColor(bgr_red, cv2.COLOR_BGR2HSV)

    hsv_space = np.uint8([[h_s_v]])
    bgr_space = cv2.cvtColor(hsv_space, cv2.COLOR_HSV2BGR)
    b = int(bgr_space[0, 0, 0])
    g = int(bgr_space[0, 0, 1])
    r = int(bgr_space[0, 0, 2])
    return (b, g, r)

def drawPixels(dictionary_to_draw, image):
    for pixel in dictionary_to_draw:
        #print(pixel)
        x, y = pixel.split((", "))
        _, x = x.split("(")
        y, _ = y.split(")")
        x = int(x)
        y = int(y)
        #print(x, y)
        total_value_for_this_pixel = 0
        for t_string in dictionary_to_draw[pixel]:
            value_for_this_string = dictionary_of_strings[str(t_string)]
            total_value_for_this_pixel += value_for_this_string

        image[y, x] = total_value_for_this_pixel
        '''
        strings_for_pixel = dictionary_of_pixels[pixel]
        for t_string in strings_for_pixel:
            if t_string in dictionary_of_strings.keys():
                number_of_strings = dictionary_of_strings[t_string]
                number_of_strings += 1
                dictionary_of_strings[t_string] = number_of_strings
            else:
                number_of_strings = 1
                dictionary_of_strings[t_string] = number_of_strings
        '''

def assignValuesToStrings(inverted_image):
    for y in range(len(inverted_image)):
        for x in range(len(inverted_image[y])):
            pixel = str((x, y))
            if pixel in dictionary_of_pixels.keys():
                strings_for_pixel = dictionary_of_pixels[pixel]
                number_of_strings = len(strings_for_pixel)
                for individual_string in strings_for_pixel:
                    t_string = str(individual_string)
                    if t_string in dictionary_of_strings.keys():
                        number_of_strings = dictionary_of_strings[t_string]
                        number_of_strings += 1 / ((inverted_image[y, x] + 1))
                        dictionary_of_strings[t_string] = number_of_strings
                    else:
                        number_of_strings = 1
                        dictionary_of_strings[t_string] = number_of_strings          
            else:
                #print("false, because " + pixel)          
                pass


cvWindows()
list_of_strings = []
coords = []
cv2.rectangle(frame, (0, 0), (frame_width, frame_height), (20, 20, 20), -1)

connectPoints(number_of_points)
resized_image = resizeImage(gray)

pixels_to_keep, pixels_to_remove = cutCircle(resized_image)
cut_out_image = blackOutPixels(pixels_to_remove, resized_image)

#print(list_of_strings)

for string in list_of_strings:
    pixelsInaLine(string)
#print(dictionary_of_pixels)
inverted_image = invertThisImage(cut_out_image)

assignValuesToStrings(inverted_image)

drawPixels(dictionary_of_pixels, cut_out_image)
#print("this stuff right here is: " + str(len(dictionary_of_pixels["(500, 500)"])))
for t_string in dictionary_of_strings:
    value_for_this_string = dictionary_of_strings[t_string]
    p1, p2 = string
    makeString(p1, p2, (value_for_this_string, value_for_this_string, value_for_this_string))

print("dictionary of strings:")
print(dictionary_of_strings)

while(1):
    #angle_x = cv2.getTrackbarPos("rotation about x", "frame")
    cv2.imshow("resized", resized_image)
    cv2.imshow("cut out", cut_out_image)
    cv2.imshow('strings', frame)


    key_value = cv2.waitKey(30)
    if key_value == ord('q'):
        break