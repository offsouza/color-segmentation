import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False, help="Path to the image")
args = vars(ap.parse_args())

def equalHistColor (img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])    
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)    
    return img_output 

def click_and_crop(event, x, y, flags, param):    
    global x_start, y_start, x_end, y_end, cropping, getROI    
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y    
    elif event == cv2.EVENT_LBUTTONUP:        
        x_end, y_end = x, y
        cropping = False
        getROI = True

x_start, y_start, x_end, y_end = 0, 0, 0, 0
cropping = False
getROI = False
refPt = []

image = cv2.imread(args["image"])
#image = equalHistColor(image)
clone = image.copy()
 
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

while True:
    i = image.copy()
    if not cropping and not getROI:
        cv2.imshow("image", image)
    elif cropping and not getROI:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        cv2.imshow("image", i)
    elif not cropping and getROI:
        cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF     
    if key == ord("r"):
        image = clone.copy()
        getROI = False 
        break    
    elif key == ord("c"):
        break

refPt = [(x_start, y_start), (x_end, y_end)]
if len(refPt) == 2:
    roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    hsvRoi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    print('min H = {}, min S = {}, min V = {}; max H = {}, max S = {}, max V = {}'.format(hsvRoi[:,:,0].min(), hsvRoi[:,:,1].min(), hsvRoi[:,:,2].min(), hsvRoi[:,:,0].max(), hsvRoi[:,:,1].max(), hsvRoi[:,:,2].max()))
   
cv2.destroyAllWindows()