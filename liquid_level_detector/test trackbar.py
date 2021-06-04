import cv2

def track_th(x):
    print("thershold: ",x)

cv2.namedWindow('trackbar')
cv2.createTrackbar('min','trackbar',0,255,track_th)

img = cv2.imread('../images/proris.png')
img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)


while True:

    th_adaptive = cv2.getTrackbarPos('a-th-min', 'trackbar')
    bottle_threshold = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                 cv2.THRESH_BINARY, th_adaptive, 5)
    cv2.imshow("img_thresh", bottle_threshold)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

