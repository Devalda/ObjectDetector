import imutils
import numpy as np
import cv2 as C
import cv2


# coloring
img = C.imread("../../images/proris_wthflash.png")
gray = C.cvtColor(img, C.COLOR_BGR2GRAY)
lab = C.cvtColor(img, C.COLOR_BGR2LAB)
l, a, b = C.split(lab)

# CLAHE
clahe = C.createCLAHE(clipLimit=3.0, tileGridSize=(5, 5))
cl = clahe.apply(l)
limg = C.merge((cl, a, b))

final = C.cvtColor(limg, C.COLOR_LAB2BGR)
gray = C.cvtColor(final, C.COLOR_BGR2GRAY)

# blur
blur_median = C.medianBlur(gray, 5)
blur_gauss = C.GaussianBlur(img, (7, 7), 2)

# tracing
th_adaptive = C.adaptiveThreshold(blur_median, 255, C.ADAPTIVE_THRESH_GAUSSIAN_C, C.THRESH_BINARY, 11, 2)
canny_blur_gray = C.Canny(blur_gauss, 55, 100)

# closing operation
kernel = np.ones((1, 1))
imgDial = C.dilate(canny_blur_gray, kernel, iterations=3)
imgThres = C.erode(imgDial, kernel, iterations=2)

# make ROI
cnts = C.findContours(gray, C.RETR_EXTERNAL, C.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#
# for c in cnts:v
#     x,y,w,h = C.boundingRect(c)
#     ROI = img[y:y+h, x:x+w]

slice = img[230:410, 110:430]
grey = C.cvtColor(slice, C.COLOR_BGR2GRAY)
blur_slice = C.medianBlur(grey, 5)
th_adaptive = C.adaptiveThreshold(blur_slice, 255, C.ADAPTIVE_THRESH_GAUSSIAN_C, C.THRESH_BINARY, 15, 2)

blur = C.GaussianBlur(slice, (5, 5), 0)
th_otsu = C.threshold(blur, 0, 255, C.THRESH_BINARY)


# modification - threshold
bottle_gray = cv2.cvtColor(slice , cv2.COLOR_BGR2GRAY)
bottle_gray = cv2.split(bottle_gray)[0]
bottle_gray = cv2.GaussianBlur(bottle_gray, (3, 3), 1)
cv2.imshow("gray", bottle_gray)
bottle_threshold = cv2.adaptiveThreshold(bottle_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,41,5)
bottle_threshold = cv2.bitwise_not(bottle_threshold)
bottle_threshold = imutils.skeletonize(bottle_threshold, size=(3, 3))
kernel = np.ones((3,3), np.uint8)
bottle_threshold = cv2.dilate(bottle_threshold, kernel, iterations=2)
bottle_threshold = cv2.erode(bottle_threshold, kernel, iterations=1)
cv2.imshow("kotak th ", bottle_threshold)

# RGB filter (black and white)
black = np.zeros((bottle_threshold.shape[0], bottle_threshold.shape[1], 3), np.uint8)
cv2.imshow("black", black)
black1 = cv2.rectangle(black,(0, 90),(290, 450),(255, 255, 255), -1)
gray = cv2.cvtColor(black,cv2.COLOR_BGR2GRAY)
ret,b_mask = cv2.threshold(gray,127,255, 0)

fin = cv2.bitwise_and(bottle_threshold,bottle_threshold,mask = b_mask) #masking image

cv2.imshow("mask",fin)


# bbox on ROI
contours = C.findContours(grey, C.RETR_EXTERNAL, C.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
areas = [C.contourArea(contour) for contour in contours]
(contours, areas) = zip(*sorted(zip(contours, areas), key=lambda a: a[1]))
bottle_clone = img.copy()
x, y, w, h = C.boundingRect(contours[-1])

print(w, h)
x = 110
y = 230
bbox = C.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

C.imshow("image", bbox)
C.waitKey(0)
