import cv2
from liquid_level_detector.ROI.tools_selector.select_roi_solo import roi_solo

def Tracking(x):
    pass

cv2.namedWindow('Threshold Control')
cv2.createTrackbar('Min', 'Threshold Control', 0, 255, Tracking)

path = "../images/proris_new/p3.png"
img = cv2.imread(path)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

roi = None
slice_image = None

if roi is None:
    rois = roi_solo.select_roi(path)
    print(rois)
    for r in range(len(rois)) :
        x = r[0]
        y = r[1]
        a = r[2]
        b = r[3]
    print(roi)

slice_image = img_gray
print(x ,y , a , b)

while True:
    thrs_min = cv2.getTrackbarPos('Min', 'Threshold Control')
    ret, thresh = cv2.threshold(img_gray, thrs_min, 255, cv2.THRESH_OTSU)
    cv2.imshow("img_thresh", thresh)

    if cv2.waitKey(1) and 0xFF == ord('q'):
        break



cv2.destroyAllWindows()