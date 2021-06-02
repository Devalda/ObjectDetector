import cv2
import numpy as np
import argparse
import glob

# image = 'R_1.png'
# image = cv2.imread(image)


class canny():

    def getContours(image, cThr=[48,100] , showCanny=False ):
        imgGray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray , (1,3) , 2)
        imgCanny = cv2.Canny(imgBlur, cThr[0],cThr[1])
        kernel = np.ones((1,1))
        imgDial = cv2.dilate(imgCanny , kernel, iterations=3)
        imgThres = cv2.erode(imgDial , kernel , iterations=2)
        if showCanny:
            cv2.imshow('Canny' , imgThres)

    def auto_canny(image, sigma=0.33):

        # compute the median of the single channel pixel intensities
        v = np.median(image)
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)
        return edged


    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--images", required=True,
                    help="path to input dataset of images")
    args = vars(ap.parse_args())
    # loop over the images
    for imagePath in glob.glob(args['R_1.png']):
        # load the image, convert it to grayscale, and blur it slightly
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        # apply Canny edge detection using a wide threshold, tight
        # threshold, and automatically determined threshold
        wide = cv2.Canny(blurred, 10, 200)
        tight = cv2.Canny(blurred, 225, 250)
        auto = auto_canny(blurred)
        # show the images
        cv2.imshow("Original", image)
        cv2.imshow("Edges", np.hstack([wide, tight, auto]))
        cv2.waitKey(0)
