import cv2 as cv2
from cv2 import cv2
import numpy as np
import math as m

def nothing(x):
    pass

def bgr_to_hsv(b_g_r):

    #bgr_red = np.uint8([[[0, 0, 255]]])
    #hsv_red = cv2.cvtColor(bgr_red, cv2.COLOR_BGR2HSV)

    bgr_space = np.uint8([[b_g_r]])
    hsv_space = cv2.cvtColor(bgr_space, cv2.COLOR_BGR2HSV)
    h = hsv_space[0, 0, 0]
    s = hsv_space[0, 0, 1]
    v = hsv_space[0, 0, 2]
    #print(hsv_space)
    return(h, s, v)

def hsv_to_bgr(h_s_v):
    hsv_space = np.uint8([[h_s_v]])
    bgr_space = cv2.cvtColor(hsv_space, cv2.COLOR_HSV2BGR)
    b = bgr_space[0, 0, 0]
    g = bgr_space[0, 0, 1]
    r = bgr_space[0, 0, 2]
    return(b, g, r)

def cutAndResize(img, dimensions):
    print("")
    orig_height = len(img)
    orig_width = len(img[0])
    print("original height: " + str(orig_height))
    print("original width: " + str(orig_width))
    if orig_height > orig_width:
        difference = orig_height - orig_width
        if (difference%2) == 0:     #if able to cut evenly on left and right
            cut = np.delete(img, slice(0, int(difference/2)), 0)
            cut = np.delete(cut, slice(int(len(cut) - difference/2), int(len(cut))), 0)

    elif orig_width > orig_height:
        difference = orig_width - orig_height
        if (difference%2) == 0:
            cut = np.delete(img, slice(0, int(difference/2)), 1)
            cut = np.delete(cut, slice(int(len(cut[0]) - difference/2), int(len(cut[0]))), 1)

    cut = cv2.resize(cut, dimensions)
    print("height: " + str(len(cut)))
    print("width: " + str(len(cut[0])))
    return(cut)

def trimImageToUnit(img, unit):
    height = len(img)
    width = len(img[0])
    difference_height = height%unit
    difference_width =  width%unit

    img = np.delete(img, slice(0, int(difference_height/2)), 0)
    img = np.delete(img, slice(int(len(img) - difference_height/2), int(len(img))), 0)

    img = np.delete(img, slice(0, int(difference_width/2)), 1)
    img = np.delete(img, slice(int(len(img[0]) - difference_width/2), int(len(img[0]))), 1)

    return(img)

def turnMonoChromatic(img, hue, sat, val, hue_percent, sat_percent, val_percent):
    
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if hue is not None:
        img[:, :, 0] = hue * hue_percent + img[:, :, 2] * (1-hue_percent)
    if sat is not None:
        img[:, :, 1] = sat * sat_percent + img[:, :, 2] * (1-sat_percent)
    if val is not None:
        img[:, :, 2] = val * val_percent + img[:, :, 2] * (1-val_percent)

    bgr_mono = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    return(bgr_mono)

def constructBlocks(block, img_to_construct):
    image = img_to_construct
    blocks_width = m.floor(len(image[0]) / block_size)
    blocks_height = m.floor(len(image) / block_size)

    row_of_blocks = block
    for new_block in range(blocks_width - 1):
        row_of_blocks = np.concatenate((row_of_blocks, block), 1)
    constructed_image = row_of_blocks
    for new_row in range(blocks_height - 1):
        constructed_image = np.concatenate((constructed_image, row_of_blocks), 0)
    return(constructed_image)

cv2.namedWindow("values")
cv2.createTrackbar("hue", "values", 90, 180, nothing)
cv2.createTrackbar("sat", "values", 90, 255, nothing)
cv2.createTrackbar("val", "values", 90, 255, nothing)
cv2.createTrackbar("hue p", "values", 100, 100, nothing)
cv2.createTrackbar("sat p", "values", 82, 100, nothing)
cv2.createTrackbar("val p", "values", 54, 100, nothing)

block_size = 100

block_paths = list(
    r"C:\Users\spenc\Downloads\better_wade.jpg"
    )
image_path = r"C:\Users\spenc\Downloads\me3.jpg"
#wide_flower_path = r"C:\Users\spenc\Downloads\download.jpg"
list_of_blocks = []
for block_image in block_paths:
    block = cv2.imread(block_image)  #building "blocks" image will be made of 
    block = cutAndResize(block, (block_size, block_size))
    list_of_blocks.append(block)

image = cv2.imread(image_path)  
image = trimImageToUnit(image, block_size)#image that wants to be constructed
#wide_flower = cv2.imread(wide_flower_path)
#im_b, im_g, im_r = cv2.split(image) #splits into blue, green, red channels
#im_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#im_hue, im_sat, im_val = cv2.split(im_hsv)

#im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#im_hue = im_hsv[:,:,0]
def createMosaic(h_p, s_p, v_p):
    list_of_chunks = []
    for y_chunk in range(int(len(image) / block_size)):
        this_row = []
        for x_chunk in range(int(len(image[0]) / block_size)):
                this_chunk = image[(y_chunk) * block_size: (y_chunk + 1) * block_size, (x_chunk) * block_size : (x_chunk + 1) * block_size]
                avg_pixel = cv2.mean(this_chunk)
                #hue, sat, val, _ = avg_pixel
                hue, sat, val= bgr_to_hsv(avg_pixel)
                identity = (x_chunk, y_chunk)
                list_of_chunks.append((identity, avg_pixel))
                #print(avg_pixel)
                cv2.rectangle(image, ((x_chunk) * block_size, (y_chunk) * block_size), ((x_chunk + 1) * block_size, (y_chunk + 1) * block_size), avg_pixel, -1)
                
                colored_block = turnMonoChromatic(block, hue, sat, val, h_p, s_p, v_p)
                if x_chunk == 0:
                    this_row = colored_block
                else:
                    this_row = np.concatenate((this_row, colored_block), 1)
        if y_chunk == 0:
            final_tiled = this_row
        else:
            final_tiled = np.concatenate((final_tiled, this_row), 0)
    return final_tiled

image = cv2.imread(image_path)  

scale_percent = 100 # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
 
image = trimImageToUnit(image, block_size)#image that wants to be constructed
hue = cv2.getTrackbarPos('hue', 'values')
sat = cv2.getTrackbarPos('sat', 'values')
val = cv2.getTrackbarPos('val', 'values')

hue_p = cv2.getTrackbarPos('hue p', 'values') / 100
sat_p = cv2.getTrackbarPos('sat p', 'values') / 100
val_p = cv2.getTrackbarPos('val p', 'values') / 100

b, g, r = hsv_to_bgr((hue, sat, val))
cv2.rectangle(image, (0, 0), (20, 20), (int(b), int(g), int(r)), -1 )

#block = turnMonoChromatic(block, hue, sat, val, hue_p, sat_p, val_p)
#constructed_image = constructBlocks(block, image)

final_tiled = createMosaic(hue_p, sat_p, val_p)
bgr_mono = turnMonoChromatic(image, hue, sat, val, 1, 0, 1)

cv2.imwrite(r"C:\Users\spenc\Documents\eeeee.jpg", final_tiled)

while True:


    cv2.imshow("original", image)
    cv2.imshow("block", block)
    cv2.imshow("monochromatic", bgr_mono)
    cv2.imshow("final_tiled", final_tiled)
    key_value = cv2.waitKey(30)
    if key_value == ord('q'):
        break