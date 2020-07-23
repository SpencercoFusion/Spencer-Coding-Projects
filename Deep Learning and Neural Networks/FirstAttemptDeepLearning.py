import numpy as np 
import math as m
import time 
import cv2
import random
import os

def createImage(x, size):
    for i in range(x):
        im = np.zeros(shape=size, dtype=np.uint8)
        if random.randint(0, 1) == 0:
            p1 = (random.randint(0, size[1] - 1), random.randint(0, size[0] - 1))
            p2 = (random.randint(0, size[1] - 1), random.randint(0, size[0] - 1))

            cv2.rectangle(im, p1, p2, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), -1)
            status = "1"
        else:
            center = (random.randint(0, size[1] - 1), random.randint(0, size[0] - 1))
            radius = random.randint(0, min( abs(center[0] - size[1]), abs( center[0]), abs(center[1] - size[0]), abs(center[1])  ))
            cv2.circle(im, center, radius, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), -1)
            status = "0"
        cv2.imwrite(trainingImagesPath + "\\" + status + "_" + str(i) + ".jpg", im)

def createFeatureVectors():
    X = []
    for file in os.listdir(trainingImagesPath):
        if file.endswith(".jpg"):
            im = cv2.imread(trainingImagesPath + "\\" + file)
            im_height, im_width, im_depth = np.shape(im)
            isRectangle = file.split("_")[0]
            featureVec = im.reshape(im_height * im_width * im_depth, 1)
            X.append(featureVec)

    np.savetxt("featureVectors.txt", featureVec)

trainingImagesPath = r"C:\Users\spenc\Documents\GitHub\Spencer-Coding-Projects\Deep Learning and Neural Networks\CirclesAndRectangles"

createImage(5, (25, 25, 3))
createFeatureVectors()


