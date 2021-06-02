import cv2
from matplotlib import pyplot as plt
import imutils

print("start")
# read image and take first channel only
img = cv2.imread("proris.png")
bottle_gray = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
cv2.imshow("color_changer",bottle_gray)

bottle_gray = cv2.split(bottle_gray)[0]

# bottle_gray = cv2.GaussianBlur(bottle_gray, (7, 7), 1)
# cv2.imshow("gray", bottle_gray)

# histogram, set manual for threshold
# plt.hist(bottle_gray.ravel(), 256,[0, 256]); plt.show()

# threshold , manual ?
T, bottle_threshold = cv2.threshold(bottle_gray, 27.5, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("threshold",T)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
bottle_open = cv2.morphologyEx(bottle_threshold, cv2.MORPH_OPEN, kernel)
cv2.imshow("morphology",bottle_open)

# final contour
print("start final contouring")
contours = cv2.findContours(bottle_open.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
