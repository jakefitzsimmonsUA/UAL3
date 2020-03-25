# NAVINT MODE WIP
import cv2
import time
import os
from panorama import Stitcher
import imutils
import os
import glob
import numpy as np

pathleft = '/home/pi/Documents/WebcamTest/LeftPicsNavInt'
pathright = '/home/pi/Documents/WebcamTest/RightPicsNavInt'
img_counter = 0
avgVint = np.zeros((1,10))

while (img_counter < 10):
    #left camera 
    cam0 = cv2.VideoCapture(0)
    cv2.namedWindow("leftnavint")
    ret0, frame0 = cam0.read()
    
    cv2.imshow("leftnavint", frame0)

    img_name0 = "left_navint_{}.png".format(img_counter)
    frame0HSV = cv2.cvtColor(frame0,cv2.COLOR_BGR2HSV)
    HSV0 = frame0HSV[300,300]
    print(HSV0)
    cv2.imwrite(os.path.join(pathleft,img_name0), frame0HSV)
    print("{} written!".format(img_name0))

    cam0.release()
    cv2.destroyAllWindows()
    
    #right camera
    cam1 = cv2.VideoCapture(2)
    cv2.namedWindow("rightnavint")

    
    ret1, frame1 = cam1.read()
    
    cv2.imshow("rightnavint", frame1)

    img_name1 = "right_navint_{}.png".format(img_counter)
    frame1HSV = cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)
    HSV1 = frame1HSV[300,300]
    print(HSV1)
    cv2.imwrite(os.path.join(pathright,img_name1), frame1HSV)
    print("{} written!".format(img_name1))
    
    cam1.release()
    cv2.destroyAllWindows()
    
    V0 = HSV0[2]
    V1 = HSV1[2]
    avgVint[0,img_counter] = (int(V0) + int(V1))/2

    img_counter = img_counter +1
    
else:
    Vint = np.mean(avgVint)
    print(Vint)
    Vint = str(Vint)
    Vinitfile = open("Vprev.txt","w+")
    Vinitfile.write(Vint)
    Vinitfile.close()
    
    
