import cv2 as cv2
from cv2 import cv2
import numpy as np
import math as m

mouse_x = 0
mouse_y = 0


######################################
######################################
######################################
######################################

def hsv2bgr(h_s_v):

    #bgr_red = np.uint8([[[0, 0, 255]]])
    #hsv_red = cv2.cvtColor(bgr_red, cv2.COLOR_BGR2HSV)

    hsv_space = np.uint8([[h_s_v]])
    bgr_space = cv2.cvtColor(hsv_space, cv2.COLOR_HSV2BGR)
    b = int(bgr_space[0, 0, 0])
    g = int(bgr_space[0, 0, 1])
    r = int(bgr_space[0, 0, 2])
    return (b, g, r)

def setToDimensions(img_to_resize, dimensions): #cuts and resizes  GREY image to be size of dimensions
    orig_height = len(img_to_resize)
    orig_width = len(img_to_resize[0])
    resized_image = img_to_resize
    new_width, new_height = dimensions

    percent_width = new_width / orig_width
    percent_height = new_height / orig_height
    print("percent width " + str(int(percent_width)))
    print("percent height " + str(int(percent_height)))
    if percent_width < percent_height:
        scale_percent = percent_width 
    elif percent_height < percent_width:
        scale_percent = percent_height 
    else:
        scale_percent = percent_height
    
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)
    img_to_resize = cv2.cvtColor(cv2.resize(img, dim, interpolation = cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)


    orig_height = height
    orig_width = width

    if orig_height < new_height:
        height_buffer = np.full(( int((new_height - orig_height)/2) , orig_width), 255, dtype=np.uint8)
        resized_image = np.concatenate((height_buffer, img_to_resize, height_buffer), axis=0) 
    orig_height = len(resized_image)
    if orig_width < new_width:
        #print("this new image height is:" + str(img_height))
        width_buffer = np.full(     (orig_height,  int((new_width - orig_width)/2) ), 255, dtype=np.uint8)
        #print(str(len(width_buffer)) + " is the height of buffer")
        #print(str(len(width_buffer[0])) + " is the length of buffer")
        resized_image = np.concatenate((width_buffer, resized_image, width_buffer), axis=1) 
    return(resized_image)    


def defineStringsAndConnectPoints(number_of_points, image, color_by_value):    #makes definitions for all strings connecting all points, and draws strings
    global list_of_string_definitions
    if number_of_points > 1:
        for i in range(number_of_points - 1):
            if not color_by_value:
                color = hsv2bgr((20 * i, 180, 180))
            else:
                p2 = number_of_points
                p1 = i + 1
                color = array_of_string_values[p2, p1]
                color = (color, color, color)
            list_of_string_definitions.append(drawString(number_of_points, i + 1, color, image))
        number_of_points = number_of_points - 1
        defineStringsAndConnectPoints(number_of_points, image, color_by_value)

def drawString(id1, id2, color, image_to_draw):         #draws the string by its definition
    p1 = pointToCoord(id1)
    p2 = pointToCoord(id2)
    cv2.line(image_to_draw, p1, p2, color, 1)
    if id1 < id2:
        t_string = (id1, id2)
    else:
        t_string = (id2, id1)
    return(t_string)

def pointToCoord(pointID):      #converts the point value to a coordinate in (x, y)
    global center
    center_x, center_y = center
    angle = pointID * 2 * m.pi / number_of_points
    point_x = int(m.cos(angle) * radius + center_x)
    point_y = int(m.sin(angle) * radius + center_y)
    cv2.circle(blank_colored, (point_x, point_y), 1, white, -1)
    cv2.putText(blank_colored, str(pointID), (point_x, point_y), font, 0.5, white)

    return(point_x, point_y)

def invertThisImage(img_to_invert):         #inverts the image, but image must be in grayscale
    t_inverted_img = (255 - img_to_invert)
    return t_inverted_img

def distance(p1, p2):                       #absolute distance between points p1 and p2
    x1, y1 = p1
    x2, y2 = p2
    distance = m.sqrt(  (x1-x2)**2  +   (y1-y2)**2  )
    return(distance)

def valueOfLine(line_m, line_b, domain, image, string_definition):       #Value of line = avg pixel value * k
    lower_x, upper_x = domain
    if lower_x > upper_x:
        l = upper_x
        u = lower_x
        lower_x = l
        upper_x = u
        print("error with range")

    if (lower_x - upper_x) != 0:
        total_value = 0
        for x_val in range(upper_x - lower_x):
            pixel_x = lower_x + x_val
            pixel_y = int(pixel_x * line_m + line_b)
            if ((center_x - pixel_x)**2 + (center_y - pixel_y)**2) < radius**2:
                if(pixel_x < len(image[0]) and pixel_y < len(image)):
                    total_value += image[pixel_y, pixel_x]
                else:
                    pass
                    #print("out of bounds of IMAGE! point is at " + str((pixel_x, pixel_y)) + ", which is out of bounds for the image with size = " + str((len(image[0]), len(image))))

            else:
                pass
                #print("out of bounds of CIRCLE! point is at " + str((pixel_x, pixel_y)) + ", which is out of bounds for the circle with radius = " + str(radius))
        average_value = total_value / (upper_x - lower_x)
        pixels_above_average = 0
        for x_val in range(upper_x - lower_x):
            pixel_x = lower_x + x_val
            pixel_y = int(pixel_x * line_m + line_b)
            if ((center_x - pixel_x)**2 + (center_y - pixel_y)**2) < radius**2:
                if(pixel_x < len(image[0]) and pixel_y < len(image)):
                    this_pixel_value = image[pixel_y, pixel_x]
                    #print("this pixel " + str((pixel_x, pixel_y)) + " has a value of " + str(this_pixel_value) + " and average is " + str(average_value))
                    if this_pixel_value > average_value:
                        pixels_above_average += 1
        percent_above_average = int(pixels_above_average / (upper_x - lower_x) * 100)
        #print("percent above average for string " + str(string_definition) + ": " + str(percent_above_average))
        global threshold_percent
        if percent_above_average < threshold_percent:
            average_value = 0
    else:
        average_value = 0
        total_value = 0


    #print("for string " + str(string_definition) + ", range between " + str(lower_x) + " and " + str(upper_x) + " is " + str(upper_x - lower_x))
    return(average_value, total_value)

def assignValuesToStrings():
    for string in list_of_string_definitions:
        p1, p2 = string
        domain = pixelRange(string)
        m, b = stringToLine(string)
        average_value, total_value = valueOfLine(m, b, domain, inverted, string)

        array_of_string_values[p2, p1] = int(average_value)


def pixelRange(string):                             #given a string, returns the range from lower to upper x that the string is in
    center_x, center_y = center

    p1, p2 = string
    angle1 = p1 * 2 * m.pi / number_of_points
    point1_x = int(m.cos(angle1) * radius + center_x)
    point1_y = int(m.sin(angle1) * radius + center_y)
    angle2 = p2 * 2 * m.pi / number_of_points
    point2_x = int(m.cos(angle2) * radius + center_x)
    point2_y = int(m.sin(angle1) * radius + center_y)
    #print("range for string " + str(string) + " is " + str(point1_x) + ", " + str(point2_x))
    if point1_x < point2_x:
        return(point1_x, point2_x)
        domain = (point1_x, point2_x)
    else:
        return(point2_x, point1_x)
        domain = (point2_x, point1_x)

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

def cursor_event(event, x, y, flags, param):
    global mouse_x
    global mouse_y
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_x = x
        mouse_y = y

def colorPixelsInaLine(line_m, line_b, domain, image, string_definition):
    string_val = array_of_string_values[string_definition[1], string_definition[0]]
    #print(string_val)
    lower_x, upper_x = domain
    if lower_x > upper_x:
        l = upper_x
        u = lower_x
        lower_x = l
        upper_x = u
        print("error with range")

    if (lower_x - upper_x) != 0:
        for x_val in range(upper_x - lower_x):
            pixel_x = lower_x + x_val
            pixel_y = int(pixel_x * line_m + line_b)
            if ((center_x - pixel_x)**2 + (center_y - pixel_y)**2) < radius**2:
                if(pixel_x < len(image[0]) and pixel_y < len(image)):
                    #print("pixel " + str((pixel_x, pixel_y)) + " is " + str(image[pixel_y, pixel_x]) + ". adding " + str(string_val))
                    image[pixel_y, pixel_x] += int(string_val)
    return(image)

def colorAllPixels(image):
    for string in list_of_string_definitions:
        p1, p2 = string
        domain = pixelRange(string)
        m, b = stringToLine(string)
        image = colorPixelsInaLine(m, b, domain, image, string)
    return image


######################################
######################################
######################################
######################################
threshold_percent = 55

frame_height = 1000
frame_width = 1000

number_of_points = 40
center = (frame_width/2, frame_height/2)
center_x, center_y = center
radius = 400

font = cv2.FONT_HERSHEY_SIMPLEX
green = (255, 0, 0)
blue = (0, 255, 0)
red = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

number_of_rows = number_of_points - 1
#path = "/home/remoteadmin/Downloads/circle.png"
#path = r"C:\Users\spenc\Downloads\Anchor-Link.png"   #image path
path = r"C:\Users\spenc\Downloads\man-21.jpg"   #image path
img = cv2.imread(path)
img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   #the gray imported image image

list_of_string_definitions = [] #the list of string definitions, where each string is defined as two points it goes through
array_of_string_values = np.zeros(((number_of_points + 1), (number_of_points + 1))) #this is a two dimensional array, where each (x, y) is a string definition, and the value at (x, y) is the value for that string

blank_colored = np.zeros(shape=(frame_height, frame_width, 1), dtype=np.uint8)  #this is just a blank_colored black screen. Used for drawing strings on
final_strings =  np.zeros(shape=(frame_height, frame_width, 3), dtype=np.uint8) 



resized = setToDimensions(img_g, (frame_width, frame_height))
inverted = 255 - resized
defineStringsAndConnectPoints(number_of_points, blank_colored, False)
assignValuesToStrings()

#defineStringsAndConnectPoints(number_of_points, final_strings, True)
final_strings = colorAllPixels(final_strings)
######################################
######################################
######################################
######################################
print(array_of_string_values)
while(1):
    cv2.setMouseCallback("final strings", cursor_event)
    cv2.setMouseCallback("strings", cursor_event)

    cv2.putText(final_strings, str((mouse_x, mouse_y)), (30, frame_height - 30), font, 1, white)
    cv2.putText(blank_colored, str((mouse_x, mouse_y)), (30, frame_height - 30), font, 1, white)


    cv2.imshow("original image", img)
    cv2.imshow("resized image", resized)
    cv2.imshow("strings", blank_colored)
    cv2.imshow("final strings", final_strings)
    cv2.imshow("inverted", inverted)

    cv2.putText(final_strings, str((mouse_x, mouse_y)), (30, frame_height - 30), font, 1, black)
    cv2.putText(blank_colored, str((mouse_x, mouse_y)), (30, frame_height - 30), font, 1, black)

    key_value = cv2.waitKey(30)
    if key_value == ord('q'):
        break