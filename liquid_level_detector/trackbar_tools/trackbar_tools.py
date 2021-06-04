import cv2
import numpy as np

# HEADER
window_name = "trackbar_tools"
value = {'th': 0, 'min': 0, 'max': 0}
disp_val = np.zeros((50,500,3), np.uint8)
cv2.namedWindow(window_name)

# display value_trackbar setting
font = cv2.FONT_HERSHEY_SIMPLEX
disp_val = cv2.putText(disp_val, "th: ", (10, 30), font, 0.5, (255,255,255), 1)
disp_val = cv2.putText(disp_val, "min: ", (90, 30), font, 0.5, (255,255,255), 1)
disp_val = cv2.putText(disp_val, "max: ", (170, 30), font, 0.5, (255,255,255), 1)

disp_val = cv2.putText(disp_val, "0", (30, 30), font, 0.5, (255,255,255), 1)
disp_val = cv2.putText(disp_val, "0", (125, 30), font, 0.5, (255,255,255), 1)
disp_val = cv2.putText(disp_val, "0", (210, 30), font, 0.5, (255,255,255), 1)


def nothing(x):
    pass

# value display updater
def update_th_value(x):
    global font, disp_val, value
    disp_val = cv2.putText(disp_val, f"{value['th']}", (30, 30), font, 0.5, (0,0,0), 1)
    disp_val = cv2.putText(disp_val, f"{x}", (30, 30), font, 0.5, (255,255,255), 1)
    value['th'] = x

def update_min_value(x):
    global font, disp_val, value
    disp_val = cv2.putText(disp_val, f"{value['min']}", (125, 30), font, 0.5, (0,0,0), 1)
    disp_val = cv2.putText(disp_val, f"{x}", (125, 30), font, 0.5, (255,255,255), 1)
    value['min'] = x

def update_max_value(x):
    global font, disp_val, value
    disp_val = cv2.putText(disp_val, f"{value['max']}", (210, 30), font, 0.5, (0,0,0), 1)
    disp_val = cv2.putText(disp_val, f"{x}", (210, 30), font, 0.5, (255,255,255), 1)
    value['max'] = x


# create trackbar
cv2.createTrackbar("th", window_name, 0 ,255, update_th_value)
cv2.createTrackbar("min", window_name, 0 ,255, update_min_value)
cv2.createTrackbar("max", window_name, 0 ,255, update_max_value)


# BODY

img = cv2.imread("proris_background.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# run
while (1):
    track_bar = cv2.imshow(window_name,disp_val)
    th = cv2.getTrackbarPos("th", window_name)
    min = cv2.getTrackbarPos("min", window_name)
    max = cv2.getTrackbarPos("max", window_name)


    ret, thresh = cv2.threshold(img_gray, min, max, cv2.THRESH_OTSU)
    cv2.imshow("img_thresh", thresh)

    key = cv2.waitKey(0) & 0xff
    if key == ord('q'):
        break



cv2.destroyAllWindows()