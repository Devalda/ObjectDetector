import cv2 as cv
import numpy as np


def sort_contours(cnts, method="top-to-bottom"):
    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    boundingBoxes = [cv.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return (cnts, boundingBoxes)

#########################################################################################

img = cv.imread('../images/micorlax_ex/mx2.jpg')
image = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# convert to grayscale
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
gaus = cv.GaussianBlur(gray, (7, 7), 2)
ret, binary = cv.threshold(gaus, 80, 255, cv.THRESH_BINARY_INV)
kernel = np.ones((5, 5), np.uint8)
dilate = cv.dilate(binary, kernel, iterations=1)

roi1 = (555, 865, 1383, 396)
y1 = int(roi1[1])
y2 = int(roi1[1] + roi1[3])
x1 = int(roi1[0])
x2 = int(roi1[0] + roi1[2])
img1 = img.copy()
img_roi1 = dilate[y1:y2, x1:x2]
cropped1 = img[y1:y2, x1:x2]
cropped2 = img[y1:y2, x1:x2]
cropped3 = img[y1:y2, x1:x2]
height, width, channels = img.shape
cropped_area = {'h': height, 'w': width, 'c': channels}


edged = cv.Canny(img_roi1, 30, 200)
contours, hierarchy = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

cnts_line,boundingBoxes = sort_contours(contours, method="top-to-bottom")
cnt_ed = max(contours, key=cv.contourArea)

areas = [cv.contourArea(c) for c in contours]
max_index = np.argmax(areas)
# print(f"max index : {max_index}")``

cnt=cnts_line[0]


x1, y1, w1, h1 = cv.boundingRect(cnt_ed)
x2, y2, w2, h2 = cv.boundingRect(cnt)

print(f"brect 1 = x:{x1} , y:{x1} , w:{w1} , h:{h1}")
print(f"brect 2 = x:{x2} , y:{x2} , w:{w2} , h:{h2}")

cv.rectangle(cropped1, (x1, y1), (x1+ w1, y1 + h1), (255,255,255), 5)
cv.rectangle(cropped1, (x2, y2), (x2+ w2, y2 + h2), (255,255,0), 5)

cv.imshow("the longest contour", cropped1)
cv.waitKey(0)