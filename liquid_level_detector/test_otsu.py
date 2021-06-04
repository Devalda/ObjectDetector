import cv2 as cv
import numpy as np

img = cv.imread('../images/Th1.png', 0)
# global thresholding

img = img.astype('uint8')

ret2,th2 = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

cv.imshow("test",th2)
cv.waitKey(0)