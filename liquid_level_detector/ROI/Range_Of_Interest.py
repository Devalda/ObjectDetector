import imutils
import numpy as np
import cv2 as C
from object_measurment.test_mx.canny_compe import canny
import image_bbox_slicer

# coloring
img = C.imread("proris_wthflash.png")
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
# cnts = C.findContours(gray, C.RETR_EXTERNAL, C.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
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


# set_canny = C.Canny(th_otsu,blur_slice,55, 100)

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = C.Canny(image, lower, upper)
    return edged


image = slice

keny = auto_canny(image)
C.imshow("canny", keny)

# C.imshow("morph_bottle",th_otsu)

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
