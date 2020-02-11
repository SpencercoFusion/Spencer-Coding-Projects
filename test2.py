import cv2
from cv2 import cv2

block_paths = r"C:\Users\spenc\Downloads\wade1.jpg"
image_path = r"C:\Users\spenc\Downloads\Spencer.jpg"

block = cv2.imread(block_paths)
image = cv2.imread(image_path)
while(1):
    cv2.imshow('image',image)

    
    key_value = cv2.waitKey(30)
    if key_value == ord('q'):
        break
cv2.destroyAllWindows()