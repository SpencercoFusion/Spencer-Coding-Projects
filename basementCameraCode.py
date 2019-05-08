import cv2
import numpy as np

frame_width = 640
frame_height = 480

frame = np.zeros(shape=(frame_width, frame_height, 3), dtype=np.uint8)
_, frame = cvsink.grabFrame(frame)

hsv = cv2.cvtColor