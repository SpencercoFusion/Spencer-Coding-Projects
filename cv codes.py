import cv2
import cscore as cs
import numpy as np

if hasattr(cs, 'UsbCamera'):
    camera = cs.UsbCamera('usbcam', camera_path)
    camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 640, 480, 30)
    #camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)



cvsink = cs.CvSink('cvsink')
cvsink.setSource(camera)

while(1):
    frame = np.zeros(shape=(640, 480, 3), dtype=np.uint8)
    _, frame = cvsink.grabFrame(frame)