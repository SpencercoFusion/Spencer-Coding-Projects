from cv2 import cv2
import numpy as np

scaleFactor = 6
radius = 30
size = 1000
center = 0
window = np.zeros(shape=(size, size, 3), dtype=np.uint8)

centerPoint = (300, 300)
boxRadius = 5


file = open('circleTest.txt', 'r')

i = 0
lines = file.readlines()
cv2.circle(window, (scaleFactor , scaleFactor * (radius + 1)), radius * scaleFactor, (0, 0, 255))
while True:
    cv2.imshow('window', window)
    t = 1
    for l in range(i):
        line = lines[l]
        split1 = line.split('radians = ')
        f = split1[0].split(' ')
        x = int(f[0]) + 1
        y = int(f[1]) + 1
        xn = scaleFactor * x
        yn = scaleFactor * y
        if i == t:
            cv2.putText(window, str(t), (xn, yn), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (100, 100, 200))
        cv2.rectangle(window, ((int(scaleFactor * x + scaleFactor/2)), int(center + (scaleFactor * y + scaleFactor/2))), (int((scaleFactor * x - scaleFactor/2)), int(center + (scaleFactor * y - scaleFactor/2))), (255, 255, 255))
        #cv2.putText(window, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.1, (255, 0, 255))
        t += 1
    if i + 1<= len(lines):
        i += 1

    k = cv2.waitKey(40)
    if k == ord('q'):
        break
