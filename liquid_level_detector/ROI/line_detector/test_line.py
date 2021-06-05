import cv2
import numpy as np

x1 = 196
y1 = 134
x2 = 338
y2 = 134

# [[196 134 237 134]]]
# (306, 742, 338, 261)

img = cv2.imread("../../../images/proris_new/p3.png")

crop =img[742:1003, 306:644]
line = cv2.line(crop, (0,y1), (644,y2), (0,0,255), 2)
cv2.imshow("line", line)
cv2.waitKey(0)