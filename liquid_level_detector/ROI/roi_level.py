import imutils
import cv2
import numpy as np

# trackbar leveling

def th_a(x):
    print("threshold adaptive",x )

cv2.namedWindow('trackbar')
cv2.createTrackbar('a-th-min','trackbar',0,255,th_a)

th_adaptive = cv2.getTrackbarPos('a-th-min', 'trackbar')

# image process
img = cv2.imread('../../images/proris_background.png')
bottle_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
bottle_gray = cv2.split(bottle_gray)[0]
bottle_gray = cv2.GaussianBlur(bottle_gray, (3, 3), 1)

while True:

    bottle_threshold = cv2.adaptiveThreshold(bottle_gray,th_adaptive,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,41,5)
    bottle_threshold = cv2.bitwise_not(bottle_threshold)
    bottle_threshold = imutils.skeletonize(bottle_threshold, size=(5, 5))
    cv2.imshow("Th-adaptive", bottle_threshold)
    if cv2.waitKey(1) and 0xFF == ord('c'):
        break

# kernel = np.ones((3,3), np.uint8)
# bottle_threshold = cv2.dilate(bottle_threshold, kernel, iterations=2)
# bottle_threshold = cv2.erode(bottle_threshold, kernel, iterations=1)

# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# bottle_open = cv2.morphologyEx(bottle_threshold, cv2.MORPH_CLOSE, kernel)


# # ROI ranger
# ROI = bottle_threshold[230:410, 110:430]
# cv2.imshow("slice morph", ROI)
#
#
# # line detector inside ROI
# min_line_length = 100
# max_line_gap = 30
#
# roi = list(map(int, ROI)) # Convert to int for simplicity
# cropped = bottle_gray[ROI[1]:ROI[1]+roi[3], ROI[0]:ROI[0]+ROI[2]]
#
# lines = cv2.HoughLinesP(ROI,1,np.pi/180,100,min_line_length,max_line_gap)
# for x in range(0, len(lines)):
#     for x1,y1,x2,y2 in lines[x]:
#         cv2.line(img,(x1,y1),(x2,y2),(237,149,100),2)
#
# cv2.imshow("hasil", img)
