import cv2
import time
import os
from panorama import Stitcher
import imutils
import os
import glob
import board
import busio
import adafruit_pca9685
import time

#i2c = busio.I2C(board.SCL, board.SDA)
#print(i2c.scan())
#pca = adafruit_pca9685.PCA9685(i2c,address=0x60)

#led_channel = pca.channels[0]

#pca.frequency = 400

pathleft = '/home/pi/Documents/L3Program/LeftPics'
pathright = '/home/pi/Documents/L3Program/RightPics'

#led_channel.duty_cycle = 0x3333
#time.sleep(2)

#capture loop - can be changed to single loop for use in mission
img_count_file = open("img_count.txt","r+")
img_counter = img_count_file.read()
img_counter = int(img_counter)

 #left camera
cam0 = cv2.VideoCapture(0)
cv2.namedWindow("left")
ret0, frame0 = cam0.read()

cv2.imshow("left", frame0)

img_name0 = "opencv_left_{}.png".format(img_counter)
cv2.imwrite(os.path.join(pathleft,img_name0), frame0)
print("{} written!".format(img_name0))

cam0.release()
cv2.destroyAllWindows()

#right camera
cam1 = cv2.VideoCapture(2)
cv2.namedWindow("right")


ret1, frame1 = cam1.read()

cv2.imshow("right", frame1)

img_name1 = "opencv_right_{}.png".format(img_counter)
cv2.imwrite(os.path.join(pathright,img_name1), frame1)
print("{} written!".format(img_name1))

cam1.release()
cv2.destroyAllWindows()
    
img_counter = img_counter + 1

#time.sleep(1)
#led_channel.duty_cycle = 0x0000
img_count_file.close()
print('Capture mode has completed.')


    
