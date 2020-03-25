#Panoramic stitching of two images
#pyimagesearch.com/2016/01/11/opencv-panorama-stitching/
#stitch.py driver script

#will be used to stitch all images following completion of all data capture

#import packages
import cv2
from panorama import Stitcher
import os
import glob

#load in folder of images
pathleft = '/home/pi/Documents/L3Program/LeftPics/*.png'
pathright = '/home/pi/Documents/L3Program/RightPics/*.png'
directory = "/home/pi/Documents/L3Program/StitchedPics"

f = glob.glob(pathleft)
imgsleft = [cv2.imread(img) for img in f]

f = glob.glob(pathright)
imgsright = [cv2.imread(img) for img in f]

#extract number of pics in folder
number_pics = len(imgsleft)

#loop images into stitcher
i = 0

while (i < number_pics):
    imageA = imgsleft[i]
    imageB = imgsright[i]

    #stitch together to create panorama
    stitcher = Stitcher()
    (result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)
  
    #save result
    resultname = "opencv_result_{}.png".format(i)
    cv2.imwrite(os.path.join(directory,resultname),result)
    keypointname = "opencv_keypoint_{}.png".format(i)
    cv2.imwrite(os.path.join(directory,keypointname),vis)
    
    if i == (number_pics - 1):
        print("Stitching mode has completed.")
        break
    
    i = i + 1

           

           