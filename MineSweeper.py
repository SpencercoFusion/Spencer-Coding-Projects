import math
import numpy as np
import cv2
import random
import argparse

'''functions:'''
def nothing(x):
   pass

def checkList(list_to_check, val ): #checks list for val, returns True if value is in list
    is_in_list = False
    for i in range(len(list_to_check)):
        if (val == list_to_check[i]):
            is_in_list = (val == list_to_check[i])
        
    return is_in_list

def getBoxNumber(coordinates): #returns the number (number of mines around) of the box at coordinates (x,y)
    value = 0
    box_x = coordinates[0]
    box_y = coordinates[1]
    if (boxes[box_y][box_x] == -1):
        value = -1
    else:
        for x in range(3):
            for y in range(3):
                if ((y + box_y - 1) >= 0) and ((x + box_x - 1) >= 0) and ((y + box_y - 1) < grid_y) and ((x + box_x - 1) < grid_x):
                    if(boxes[y + box_y - 1][x + box_x - 1] == (-1)):
                        value = value + 1
    return(value)

def pressBox(box_x, box_y): 
    global you_died
    if show_box[box_y][box_x] == 1: #if box already has status "show == 1"
        clearAround(box_x, box_y)
    elif mode != 1: #if not in flag mode
        if boxes[box_y][box_x] == -1:
            you_died = True
        else: 
            show_box[box_y][box_x] = 1

    elif mode == 1: #if in flag mode
        if flags[box_y][box_x] == 0:
            flags[box_y][box_x] = 1
            print("flags:")
            print(flags)
            print("mines:")
            print(mines_on_field)
            print("Boxes:")
            print(boxes)
        elif flags[box_y][box_x] == 1:
            flags[box_y][box_x] = 0
            print("flags:")
            print(flags)
            print("mines:")
            print(mines_on_field)
            print("Boxes:")
            print(boxes)

        
def clearAround(this_x, this_y):
    global you_died
    flags_around = 0
    for x in range(3):
        for y in range(3):
            x_new = x + this_x - 1
            y_new = y + this_y - 1
            if (x_new >= 0) and (y_new >= 0) and (x_new < grid_x) and (y_new < grid_y): 
                if flags[y_new][x_new] == 1:
                    flags_around += 1              
    if flags_around == (boxes[this_y][this_x]):   
        for x in range(3):
            for y in range(3):
                x_new = x + this_x - 1
                y_new = y + this_y - 1
                if (x_new >= 0) and (y_new >= 0) and (x_new < grid_x) and (y_new < grid_y):
                    if flags[y_new][x_new] == 0 and mines_on_field[y_new][x_new] == 1:
                        you_died = True
                    elif (flags[y_new][x_new]) != 1:
                        show_box[y_new][x_new] = 1
def mouse(event,x,y,flags,param):
    global mode 
    global previous_mode
    if event == cv2.EVENT_RBUTTONDOWN:
        if previous_mode == 1:
            mode = 0
        elif previous_mode == 0:
            mode = 1
    previous_mode = mode

    global mouse_x
    global mouse_y
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_x = x
        mouse_y = y

def begin():   
    global boxes, total_boxes, show_box, flags, mines_on_field, mines, you_died

    boxes = np.zeros((grid_x,grid_y))
    total_boxes = grid_x * grid_y

    show_box = np.zeros((grid_y,grid_x)) #grid, where 0 tells to show box and 1 hides it
    flags = np.zeros((grid_y,grid_x)) #grid, where 1 = flag and 0 = no flag
    mines_on_field = np.zeros((grid_y,grid_x)) #grid of all mines, where if there is a mine it is 1

    mines = []
    m = 0
    while (m < number_mines):
        mine_x = random.randrange(grid_x)
        mine_y = random.randrange(grid_y)
        if (checkList(mines, (mine_x, mine_y))):
            print("Uh oh! duplicate")
            m = m - 1
        else:
            mines.append((mine_x, mine_y))
            boxes[mine_y][mine_x] = -1
        m = m + 1

    for m in range(len(mines)):
        mine_x = mines[m][0]
        mine_y = mines[m][1]
        mines_on_field[mine_y][mine_x] = 1
        
    for x in range(grid_x):
        for y in range(grid_y):
            boxes[y][x] = getBoxNumber((x,y))     

    you_died = False                       
                              
'''variables:'''
you_died = False
mode = 0

grid_x = 20
grid_y = 20
box_length = 40
number_mines = 100
draw_mines = False

'''cv setup:'''
frame_height = box_length * (grid_y + 2)
frame_width = box_length * (grid_x + 2)
frame = np.zeros(shape=(frame_height, frame_width, 3), dtype=np.uint8)
font = cv2.FONT_HERSHEY_TRIPLEX
center = (frame_width/2, frame_height/2, 0)
cv2.namedWindow("original")
cv2.setMouseCallback('original', mouse)

center_x = int(frame_width/2)
center_y = int(frame_height/2)
#cv2.createTrackbar('rotation about x', 'frame', 360, frame_width, nothing)

'''oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'''
white = (255, 255, 255)
black = (0, 0, 0)
blue = (255, 0, 0)
red = (0, 0, 255)
green = (0, 255, 0)

colors = [blue, green, red, (102, 0, 0), (0, 0, 102), (255, 255, 0), (0, 0, 0), (192, 192, 192)]

mode = 0
m_key_previous = 0
mouse_x, mouse_x_pre = 0, 0
mouse_y, mouse_y_pre = 0, 0
'''oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'''
begin()

print(boxes)
print(flags)
print(mines_on_field)
'''while loop'''
while(1):
    
    
    #angle_x = cv2.getTrackbarPos("rotation about x", "frame")
    cv2.rectangle(frame, (0,0), (frame_width, frame_height), white, -1) #draws white background
    cv2.rectangle(frame, (box_length, box_length), (frame_width - box_length, frame_height - box_length), (160, 160, 160), -1) #draws gray rectangel

    center_offset_x = (frame_width - (grid_x * box_length))/2
    center_offset_y = (frame_height - (grid_y * box_length))/2

    if (mouse_x != mouse_x_pre) or (mouse_y != mouse_y_pre):
        box_x = int(round((mouse_x) * (grid_x + 2) / frame_width - 1.5, 0))
        box_y = int(round((mouse_y) * (grid_y + 2) / frame_height - 1.5, 0))
        if box_x == -0:
            box_x = 0
        if box_y == -0:
            box_y = 0
        if box_x >= 0 and box_x < grid_x and box_y >= 0 and box_y < grid_y: #checks to see if box is in grid, and not just a border
            pressBox(box_x, box_y)
        if box_x == -1 and box_y == -1: #watches for pressing restart box
            begin()
    for x in range (grid_x):
        for y in range(grid_y):
            x_start = int(x * box_length + center_offset_x)
            y_start = int(y * box_length + center_offset_y)
            x_fin = int((x * box_length) + box_length + center_offset_x)
            y_fin = int((y * box_length) + box_length + center_offset_y)
            cv2.rectangle(frame, (x_start, y_start), (x_fin, y_fin), black, 2 )
    
    for m in range(len(mines)):
        if len(mines) != number_mines:
            end = 0/0 #breaks code
        else:
            x_cord = mines[m][0]
            this_mine_x = int(x_cord * box_length + box_length/2 + center_offset_x)

            y_cord = mines[m][1]
            this_mine_y = int(y_cord* box_length + box_length/2 + center_offset_y)
            draw_mines = you_died
            if (draw_mines):
                cv2.circle(frame, (this_mine_x, this_mine_y), int(box_length/5), red, 3)

    for x in range(len(boxes)):
        for y in range(len(boxes)):
            box_number = boxes[y][x]
            
            if (box_number == -1):
                pass
            elif show_box[y][x] == 0: #checks to see if that box should be shown
                pass
            else:
                cv2.rectangle(frame, (box_length * (x + 1) + 1, box_length * (y + 1) + 1), (box_length * (x + 2) - 1, box_length * (y + 2) - 1), (240, 240, 240), -1 )
                if box_number == 0:
                    clearAround(x, y)
                else:
                    number_color = colors[int(box_number - 1)]
                    cv2.putText(frame, str(int(boxes[y][x])), (  int(x * box_length + center_offset_x + box_length * 0.25), 
                    int((y) * box_length + center_offset_y + (box_length * 0.75))  ), font, box_length/50, number_color, 1)      
    
    incorrect = 0
    for x in range(len(flags)):
        for y in range(len(flags)):
            if flags[y][x] == 1:
                cv2.putText(frame, "F", (  int(x * box_length + center_offset_x + box_length * 0.25), 
                int((y) * box_length + center_offset_y + (box_length * 0.75))  ), font, box_length/50, red, 1) 
            if flags[y][x] != mines_on_field[y][x]:
                incorrect += 1
    #print(incorrect)
                


    if you_died:
        cv2.putText(frame, "oopsie", (0, center_y), font, 4, black, 3)
        draw_mines = True

    mouse_x_pre = mouse_x
    mouse_y_pre = mouse_y

    if mode == 1:
        cv2.putText(frame, "flag", (0, frame_height - 10), font, 1, black, 2)

    cv2.imshow('original', frame)
    key_value = cv2.waitKey(30)
    if key_value == ord('q'):
        break
    #cv2.createButton("mode", button)
    #print(str(mode))