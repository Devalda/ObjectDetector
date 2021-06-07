import cv2
from matplotlib import pyplot as plt
import imutils
import numpy as np

print("start")
# read image and take first channel only
img = cv2.imread("../images/proris_new/p3.png")
bottle_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
bottle_gray = cv2.split(bottle_gray)[0]
bottle_gray = cv2.GaussianBlur(bottle_gray, (3, 3), 1)
cv2.imshow("gray", bottle_gray)

# histogram, dont know why ?ts
# plt.hist(bottle_gray.ravel(), 256,[0, 256]); plt.show()

print("start treshold")
# threshold , manual ?
# (T, bottle_threshold) = cv2.threshold(bottle_gray, 27.5, 255, cv2.THRESH_BINARY_INV)


# adaptive threshold || requires odd blocksize

bottle_threshold = cv2.adaptiveThreshold(bottle_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,41,5)
bottle_threshold = cv2.bitwise_not(bottle_threshold)
# bottle_threshold = imutils.skeletonize(bottle_threshold, size=(5, 5))


# se=cv2.getStructuringElement(cv2.MORPH_RECT , (8,8))
# bg=cv2.morphologyEx(bottle_threshold, cv2.MORPH_DILATE, se)
# out_gray=cv2.divide(bottle_threshold, bg, scale=255)
# out_binary=cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU )[1]
# cv2.imshow("out-gray",out_gray)
# cv2.imshow("out-binary",out_binary)

# kernel = np.ones((3,3), np.uint8)
# bottle_threshold = cv2.dilate(bottle_threshold, kernel, iterations=2)
# bottle_threshold = cv2.erode(bottle_threshold, kernel, iterations=1)
# cv2.imshow("dilate",bottle_threshold)


# bottle_threshold = bottle_threshold.astype('uint8')
# bottle_threshold = cv2.threshold(bottle_threshold,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
# bottle_threshold = cv2.filter2D(bottle_threshold,-2, kernel)


# erote & dilate
# kernel =np.ones((7,7), np.uint8)
# bottle_threshold = cv2.erode(bottle_threshold, kernel, iterations=1)
# bottle_threshold = cv2.dilate(bottle_threshold, kernel, iterations=1)


# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# bottle_open = cv2.morphologyEx(bottle_threshold, cv2.MORPH_CLOSE, kernel)
# cv2.imshow("morphology",bottle_open)
# cv2.waitKey(0)

cv2.imshow("threshold",bottle_threshold)

# final contour
print("start final contouring")
contours = cv2.findContours(bottle_threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
bottle_clone = img.copy()
kontur=cv2.drawContours(bottle_clone, contours, -1, (255, 0, 0), 2)
cv2.imshow("final-contours",kontur)

# sort contours by area
areas = [cv2.contourArea(contour) for contour in contours]
(contours, areas) = zip(*sorted(zip(contours, areas), key=lambda a:a[1]))
# print contour with largest area
bottle_clone = img.copy()
cv2.drawContours(bottle_clone, [contours[-1]], -1, (255, 0, 0), 2)

# draw bounding box, calculate aspect and display decision
bottle_clone = img.copy()
(x, y, w, h) = cv2.boundingRect(contours[-1])
aspectRatio = w / float(h)

print("aspect ratio : ",aspectRatio)


# set full
if aspectRatio < 0.4:
    cv2.rectangle(bottle_clone, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(bottle_clone, "Full", (x + 10, y + 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

elif aspectRatio < 0.8:
    cv2.rectangle(bottle_clone, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(bottle_clone, "half_full", (x + 10, y + 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

elif aspectRatio < 1:
    cv2.rectangle(bottle_clone, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(bottle_clone, "almost_low", (x + 10, y + 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

# set low statement
else:
    cv2.rectangle(bottle_clone, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.putText(bottle_clone, "very_Low", (x + 10, y + 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

cv2.imshow("Decision", bottle_clone)
cv2.waitKey(0)
