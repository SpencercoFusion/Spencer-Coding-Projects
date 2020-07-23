import cv2
import numpy as np 
import math as m 
import pandas as pd 
import xlsxwriter
import os
import pyautogui
import time

font = cv2.FONT_HERSHEY_DUPLEX
blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)
yellow = (0, 255, 255)

char = []
for i in range(33, 127):
    char.append(chr(i))
    #char.append(chr(32))
char = ''.join(char)
print(char)
def sortByBrightness(val):
    return val[1]
def nothing(x):
    pass
def writeAllChar():
    char_dist = 15
    font_scale = 0.4
    for x in range(127 - 33):
        cv2.putText(frame, chr(x + 33), (x * char_dist, 300), cv2.FONT_HERSHEY_DUPLEX, font_scale, (50, 50, 50))
    multiline_string = ''.join((char, '\n' , '\t', char))
    print(multiline_string)
    cv2.putText(frame, multiline_string, (10, 100), font, font_scale, (100, 100, 100))
def writeSingleChar(): 
    font_size = 1
    font_color = (255, 255, 100)
    #cv2.putText(frame, chr(48), (800, 400), font, font_size, font_color)
    for size in range(20):
        cv2.putText(frame, chr(48), (int(size * frame_width / 20), 400), font, size / 5, font_color, thickness=0)
        cv2.putText(frame, str(size / 5), (int(size * frame_width / 20), 500), font, 0.5, font_color)
def findHeightOfChar(t_frame):
    f_height, f_width, _ = t_frame.shape    

    original_frame = t_frame.copy()
    for y in range(f_height):
        row = t_frame[y]
        row_sum = sum(sum(row))
        if row_sum != 0:
            char_max_height = y
            break
    for y in range(f_height):
        y = f_height - 1 - y
        row = t_frame[y]
        row_sum = sum(sum(row))
        if row_sum != 0:
            char_min_height = y
            break

    t_frame = np.rot90(t_frame, k=1, axes=(0, 1))   #rotating frame to obtain max side lengths easier as treating them as y values
    for x in range(f_width):
        row = t_frame[x]
        row_sum = sum(sum(row))
        if row_sum != 0:
            char_right_bound = f_width - 1 - x
            break
    for x in range(f_width):
        x = f_width - 1 - x
        row = t_frame[x]
        row_sum = sum(sum(row))
        if row_sum != 0:
            char_left_bound = f_width - 1 - x
            break
    t_frame = np.rot90(t_frame, k=1, axes=(1, 0))
    char_width = char_right_bound - char_left_bound
    char_height = char_min_height - char_max_height
    #cv2.circle(t_frame, (f_width/2, f_height/2), 0, (100, 255, 255), -1)

    cv2.line(t_frame, (char_left_bound, 0), (char_left_bound, f_height), blue, 1)        #left vertical
    cv2.line(t_frame, (char_right_bound, 0), (char_right_bound, f_height), yellow, 1)    #right vertical
    cv2.line(t_frame, (0, char_max_height), (f_width, char_max_height), red, 1)         #top horizontal
    cv2.line(t_frame, (0, char_min_height), (f_width, char_min_height), green, 1)         #top horizontal
    return(original_frame, t_frame, char_width, char_height)
def writeDataToSpreadsheet():
    sizes = []
    char_widths = []
    char_heights = []

    for s in range(50):
        size = s * 22/100 
        original_frame, t_frame, char_width, char_height = findHeightOfChar('0', size)
        sizes.append(size)
        char_widths.append(char_width)
        char_heights.append(char_height)
    print(sizes)
    print(char_widths)
    print(char_heights)
    data_for_sheet = [sizes, char_widths, char_heights]
    df = pd.DataFrame(data_for_sheet).T
    df.to_excel(excel_writer = r"C:\Users\spenc\Documents\Character Sizes Opencv.xlsx")
def createTestDoc():
    width = 1
    height = 1
    full_chars = np.full((height, width), chr(64))
    top_buffer = np.full((5, width), chr(32))
    side_buffer = np.full((height + 5, 12), chr(32))
    text = np.concatenate((top_buffer, full_chars), axis=0)
    text = np.concatenate((side_buffer, text), axis=1)
    arrayToAscii(text)
    _, doubleTall_frame, char_width, char_height = findHeightOfChar(t_frame = cv2.bitwise_not(cv2.imread('500%_doubleTall_@.PNG')))
    print('Double Tall @' + '\n' + 'char_width: ' + str(char_width) + '\n' + 'char_height: ' + str(char_height) + '\n')
    _, doubleTall_frame, char_width, char_height = findHeightOfChar(t_frame = cv2.bitwise_not(cv2.imread('500%_single_@.PNG')))
    print('Single Tall @' + '\n' + 'char_width: ' + str(char_width) + '\n' + 'char_height: ' + str(char_height) + '\n')
    _, doubleTall_frame, char_width, char_height = findHeightOfChar(t_frame = cv2.bitwise_not(cv2.imread('500%_doubleWide_@.PNG')))
    print('Double Wide @' + '\n' + 'char_width: ' + str(char_width) + '\n' + 'char_height: ' + str(char_height) + '\n')
def arrayToAscii(arr):
    doc = open('ascii_test_document.txt', 'w')
    for line in arr:
        line = ''.join(line)
        doc.write(line + '\n')
    doc.close()
def createAsciiSquares():   #creates individual text files where each square is full of a single character
    for char_id in range(33, 127):
        txt_path = 'C:/Users/spenc/Documents/GitHub/Spencer-Coding-Projects/ascii/' + str(char_id) + '_ascii_square.txt'
        im_path = 'C:/Users/spenc/Documents/GitHub/Spencer-Coding-Projects/ascii/' + str(char_id) + '_ascii_square.png'
        doc = open(txt_path, 'w')
        line = ''.join(np.full((500), chr(char_id)))
        for l in range(250):
            doc.write(line + '\n')
        doc.close()
        os.startfile(txt_path)
        time.sleep(1)
        myScreenshot = pyautogui.screenshot()
        print(myScreenshot)
        myScreenshot.save(im_path)
        screenShot = cv2.imread(im_path)
        cv2.imwrite(im_path, cropAsciiSquare(screenShot))
        print(str(char_id - 32) + '/93')
def cropAsciiSquare(image):
    min_x = 410
    max_x = 1343
    min_y = 223
    max_y = 904
    cut = image[min_y:max_y, min_x:max_x]
    return(cut)
def getCharDensities():
    char_densities = []
    get_arr_avg = lambda image: int(np.sum(image) / (len(im) * len(im[0]) * len(im[0, 0])))
    for char_id in range(33,127):
        im = cv2.imread('C:/Users/spenc/Documents/GitHub/Spencer-Coding-Projects/ascii/' + str(char_id) + '_ascii_square.png')
        avg = get_arr_avg(im)
        #cv2.imshow(str(char_id) + ' id has avg: ' + str(avg), im)
        char_densities.append((char_id, avg))
        sorted_densities = char_densities.copy()
        sorted_densities.sort(key=sortByBrightness)
    return(char_densities, sorted_densities)


frame_height = 800
frame_width = 1600
frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

test_im = cv2.imread('aperature logo.jpg')

cv2.namedWindow('values')
cv2.createTrackbar('x', 'values', 0, 1920, nothing)
cv2.createTrackbar('y', 'values', 0, 1080, nothing)

densities, sorted_densities = getCharDensities()
print('\n' + 'densities:' + '\n' + str(densities))
print('\n' + 'sorted:' + '\n' + str(sorted_densities))

while(1):
    x = cv2.getTrackbarPos('x', 'values')
    y = cv2.getTrackbarPos('y', 'values')


    cv2.imshow('test_im', test_im)
    k = cv2.waitKey(20)
    if k == ord('q'):
        break

cv2.destroyAllWindows()
