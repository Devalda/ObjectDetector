import cv2
from numpy.lib import math
import numpy as np
from tools.ROI.RoiTools import select_roi


# spek botol
# tinggi botol : 9,8 cm || jarak leher botol(boddy-head): 2cm || lebar body : 3cm || lebar leher : 1cm

path = "../../../images/proris_new/p3.png"
img = cv2.imread(path)
img = np.uint8(img)
img_gray    = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur    = cv2.GaussianBlur(img_gray, (7, 7), 2)
ret, th = cv2.threshold(img_blur, 0, 255, cv2.THRESH_OTSU)
img_canny   = cv2.Canny(th, 55,110)

# closed line
kernel  = np.ones((5,5), np.uint8)
img_dil = cv2.dilate(img_canny, kernel, iterations=1)
img_ero = cv2.erode(img_dil, kernel, iterations=1)
closing = cv2.morphologyEx(img_dil, cv2.MORPH_CLOSE, kernel)

# define roi1
roi1 = cv2.selectROI("select roi 1",img)
print("roi",roi1)
y1 = int(roi1[1])
y2 = int(roi1[1]+roi1[3])
x1 = int(roi1[0])
x2 = int(roi1[0]+roi1[2])
img1 = img.copy()
img_roi1 =closing[y1:y2, x1:x2]
cropped1 = img[y1:y2, x1:x2]


# set line inside roi1
minLineLength = 800
maxLineGap = 10
lines = cv2.HoughLinesP(img_roi1,1,np.pi/180,100,minLineLength)


final_line = lines[len(lines)-1]
print(final_line)
for f in final_line:
    x1a = 0
    y1a = f[1]
    x2a = x2
    y2a = f[3]

line1 = cv2.line(cropped1, (x1a,y1a), (x2a,y2a), (255,0,0), 2)
cv2.imshow("line",line1)

# set average_indicator for liquid [within target , overfilled , underfilled]
    # todo : (wt = within target , of = overfilled , uf = underfilled)

wt = ''
of = ''
uf = ''

# create calculation and add standar deviation
height, width, channels = cropped1.shape
mean = height/2
standar_deviation_of = mean - 20
standar_deviation_uf = mean + 20


print("mean : ",mean , " y2a: ",y2a)

# add statement and create boundingbox decision
if y2a == mean:
    bbox1 = cv2.rectangle(img1, (x1, y1), (x2, y2), (0,255,0), 5)
    cv2.putText(bbox1, 'Perfect', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    cv2.imshow("Decision Box",bbox1)

elif y2a < standar_deviation_of:
    bbox1 = cv2.rectangle(img1, (x1, y1), (x2, y2), (255,0,0), 5)
    cv2.putText(bbox1, 'OverFilled', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    cv2.imshow("Decision Box",bbox1)

elif y2a > standar_deviation_uf:
    bbox1 = cv2.rectangle(img1, (x1, y1), (x2, y2), (0, 0, 255), 5)
    cv2.putText(bbox1, 'UnderFilled', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    cv2.imshow("Decision Box",bbox1)

else:
    bbox1 = cv2.rectangle(img1, (x1, y1), (x2, y2), (0,255,0), 5)
    cv2.putText(bbox1, 'within target', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    cv2.imshow("Decision Box",bbox1)


# define roi2
# roi2 = cv2.selectROI("select roi 1",img)
# print("roi",roi2)
# y1 = int(roi2[1])
# y2 = int(roi2[1]+roi2[3])
# x1 = int(roi2[0])
# x2 = int(roi2[0]+roi2[2])
# img2 = img.copy()
# img_roi2 =closing[y1:y2, x1:x2]
# bbox2 = cv2.rectangle(img2, (x1, y1), (x2, y2), (0,0,255), 5)
# cropped2 = img[y1:y2, x1:x2]
# cv2.putText(bbox1, 'LEVEL-1', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
#
#
# # set line inside roi2
# minLineLength = 800
# maxLineGap = 10
# lines2 = cv2.HoughLinesP(img_roi2,1,np.pi/180,100,minLineLength)
#
#
# final_line2 = lines2[len(lines)-1]
# print(final_line2)
# for f in final_line2:
#     x1a = 0
#     y1a = f[1]
#     x2a = x2
#     y2a = f[3]
#
# line2 = cv2.line2(cropped2, (x1a,y1a), (x2a,y2a), (255,0,0), 2)
# cv2.imshow("line",line2)




cv2.waitKey(0)