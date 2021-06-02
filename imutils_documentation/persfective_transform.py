from imutils import perspective
import numpy as np
import cv2


notecard = cv2.imread("notecard.png")
clone = notecard.copy()
pts = np.array([(73, 239), (356, 117), (475, 265), (187, 443)])

# loop over the points and draw them on the cloned image
for (x, y) in pts:
    cv2.circle(clone, (x, y), 5, (0, 255, 0), -1)

# apply the four point tranform to obtain a "birds eye view" of
# the notecard
warped = perspective.four_point_transform(notecard, pts)

# show the original and warped images
cv2.imshow("Original", clone)
cv2.imshow("Warped", warped)
cv2.waitKey(0)
