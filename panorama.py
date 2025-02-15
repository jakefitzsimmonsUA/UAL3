#Panoramic stitching of two images
#pyimagesearch.com/2016/01/11/opencv-panorama-stitching/
#define Stitcher class

#program where actual stitching takes place

#import packages
import numpy as np
import imutils
import cv2

class Stitcher:
    def __init__(self):
        #determine if OpenCV v3.x is being used
        self.isv3 = imutils.is_cv3(or_better=True)
        
    def stitch(self, images, ratio=0.75, reprojThresh=4.0, showMatches=False):
        #unpack images, detect keypoints, extract local invariant descriptors from them (must input images from left to right)
        (imageB, imageA) = images
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)
        
        #match features between two images
        M = self.matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh)
        
        #if match is None, then there are not enough matched keypoints to create panorama
        if M is None:
            return None
        
        #else, apply perspective warp to stitch images together
        (matches, H, status) = M
        result = cv2.warpPerspective(imageA, H,(imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
        
        #check to see if keypoint matches should be visualized
        if showMatches:
            vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches, status)
            
            #return tuple of stitched image and visualization
            return(result,vis)
        
        #return stitched image
        return result
    
    def detectAndDescribe(self, image):
        #convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        
        #check version of OpenCV
        if self.isv3:
            #detect and extract features from image
            descriptor = cv2.xfeatures2d.SIFT_create()
            (kps,features) = descriptor.detectAndCompute(gray,None)
            
        #else, if v2.4.x
        else:
            #detect keypoints
            detector = cv2.FeatureDetector_create("SIFT")
            kps = detector.detect(gray)
            
            #extract features
            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)
            
        #convert keypoints from KeyPoint objects to NumPy arrays
        kps = np.float32([kp.pt for kp in kps])
        
        #return tuple of keypoints and features
        return (kps,features)
    
    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
        #compute raw matches and intialize list of actual matches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []
        
        #loop over raw matches
        for m in rawMatches:
            #ensure distance is within certain ratio of each other (Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))
                
        #computing a homography requires at least 4 matches
        if len(matches) > 4:
            #construct two sets of points
            ptsA = np.float32([kpsA[i] for (_,i) in matches])
            ptsB = np.float32([kpsB[i] for (i,_) in matches])
            
            #compute homography between two sets of points
            (H,status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)
            
            #return matches along with homography matrix and status of each matched point
            return (matches, H, status)
        
        #otherwise, no homography could be computed
        return None
    
    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
        #initialize the output visualization image
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB
        
        #loop over matches
        for ((trainIdx, queryIdx), s) in zip(matches,status):
            #only process match if keypoint was successfully matched
            if s==1:
                #draw match
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)
                
        #return visualization
                return vis