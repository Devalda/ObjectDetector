import cv2
import cv2 as cv

img = cv.imread('brown_btl.png',0)

blur = cv.GaussianBlur(img,(5,5),0)
ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

cv2.imshow("otsu test",th3)
cv2.waitKey(0)