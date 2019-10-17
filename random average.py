import math
import random
import cv2
import numpy as np
def nothing(x):
   pass

frame_height = 640
frame_width = 640

font = cv2.FONT_HERSHEY_TRIPLEX
frame = np.zeros(shape=(frame_height, frame_width, 3), dtype=np.uint8)

i = 0
average = 0
how_many = 10
cap = 100
cv2.circle(frame, (640, 640), 10, (255, 0, 0) )
while(1):
    #cv2.rectangle(frame, (0,0), (frame_height, frame_width), (255, 255, 255), -1)


    if i < how_many:
        number = random.randrange(1, cap)
        average = (i * average + number) / (i + 1)
        i += 1
    else:
        cv2.putText(frame, str(average), (320, 160), font, 1, (255, 0, 255))
    cv2.circle(frame, (int(640 * i /how_many), (int(average))), 1, (255, 0, 0), 0)

    cv2.imshow('original', frame)
    key_value = cv2.waitKey(30)

    if key_value == ord('q'):
        break
