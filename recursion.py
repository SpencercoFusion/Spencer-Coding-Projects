points = []
import numpy as np
import cv2 
from cv2 import cv2

def connectPoints(number_of_points):
    if number_of_points > 0:
        for i in range(number_of_points):
           points.append((number_of_points, i))
        number_of_points = number_of_points - 1
        connectPoints(number_of_points)
    else:
        print(points)

def goThroughArray(array):
    for y in range(len(array[0])):
        for x in range(len(array[1])):
            array[y : x] = 2
    return array


first = np.full((10, 5), 10, dtype=int)
second = np.full((10, 5), 20, dtype=int)

array = np.concatenate((first, second), axis=0)


path = r'C:\Users\spenc\Downloads\apple.png'   #image path
img = cv2.imread(path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
buffer = np.full((300, 30), 30, dtype=np.uint8)
print(buffer)
new_image = np.concatenate((gray, buffer, gray), axis=1)

dictionary = {
    "(10, 20)" : 10,
    "(20, 30)" : 20,
    "(2, 2)" : 100,
}
for i in dictionary:
    x, y = i.split((", "))
    _, x = x.split("(")
    y, _ = y.split(")")
    x = int(x)
    y = int(y)
    #print(x + y)

if str((10, 20)) in dictionary.keys():
    print("true")
else:
    print("false")