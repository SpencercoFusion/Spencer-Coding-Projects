import cv2
import numpy as np 
import math as m

class Blinker():
    def __init__(self, center, num):
        self.loc = loc
        self.num = num
    
    def drawBlinker(self):
        points = []
        for i in range(6):
            theta = i * 360 / 6
            px = m.cos(theta) * blinker_radius
            py = m.sin(theta) * blinker_radius
            points.append((px, py))




f_height = 800
f_width = 800
background_brightness = 230
frame = np.full((f_height, f_width, 3), background_brightness, dtype=np.uint8)       #create gray background image

blinker_radius = 30

listOfBlinkers = []
for i in range(5):
    b = Blinker(1, str(i))
    listOfBlinkers.append(b)

while True:


    cv2.imshow('frame', frame)
    k = cv2.waitKey(30)
    if k == ord('q'):
        break