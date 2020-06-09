#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np

def equalHistColor (img):
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)        
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)      
        return img_output
    
#image = cv2.imread('./bola.jpg')
image = cv2.imread('Banco/eosi/5.bmp')

img =  equalHistColor(image)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
blur = cv2.GaussianBlur(hsv, (11, 11), 0)

lower = np.array([129,200,0])
up = np.array([160,255,255])

# lower = np.array([31,76,91])
# up = np.array([53,142,255])

mask = cv2.inRange(blur, lower, up)
kernel = np.ones((3,3),np.uint8)
res = cv2.bitwise_and(image,image, mask= mask)            

cv2.imshow("res ", res)
cv2.waitKey(0)


