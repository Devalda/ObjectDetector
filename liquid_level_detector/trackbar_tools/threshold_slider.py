import cv2

def Tracking(x):
    pass

cv2.namedWindow('Threshold Control')
cv2.createTrackbar('Min', 'Threshold Control', 0, 255, Tracking)

img = cv2.imread("proris_background.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

while True:

    thrs_min = cv2.getTrackbarPos('Min', 'Threshold Control')
    ret, thresh = cv2.threshold(img_gray, thrs_min, 255, cv2.THRESH_OTSU)
    cv2.imshow("img_thresh", thresh)

    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

cv2.destroyAllWindows()