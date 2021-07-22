import cv2
import numpy as np

img = cv2.imread("../../images/micorlax_ex/mx2.jpg")


img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh_img = cv2.threshold(img_grey, 100, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

img_contours = np.zeros(img.shape)
cv2.drawContours(img_contours, contours, -1, (0,255,0), 4)
cv2.imshow("show",img_contours)
cv2.waitKey(0)