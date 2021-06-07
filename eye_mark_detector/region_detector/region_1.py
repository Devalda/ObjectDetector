import cv2 as cv
import numpy as np

f = False
t = True


# console
roi = t
color = t
revert = t
threshold = t
image = 5

#######################

path_lib = {1:"../../images/micorlax_ex/eyemark 1.jpg" , 2:"../../images/micorlax_ex/eyemark-cut-1.jpg"
            ,3:"../../images/micorlax_ex/eyemark3.jpg", 4:"../../images/micorlax_ex/mx1.jpg"
            ,5:"../../images/micorlax_ex/mx2.jpg"}

img= cv.imread(path_lib[image])
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_blur = cv.GaussianBlur(img_gray, (3, 3), 1)


if threshold:
    # ret, th = cv.threshold(img_blur, 0, 255, cv.THRESH_OTSU)
    th = cv.adaptiveThreshold(img_blur,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,41,5)
    cv.imshow("th",th)
    if revert:
        revert_th = cv.bitwise_not(th)
        img_canny = cv.Canny(revert_th, 33, 110)
        cv.imshow("canny", img_canny)
    else:
        img_canny = cv.Canny(th, 55, 110)
        cv.imshow("canny", img_canny)
else :
    if revert:
        revert_th = cv.bitwise_not(img_blur)
        img_canny = cv.Canny(revert_th, 33, 110)
        cv.imshow("canny", img_canny)
    else:
        img_canny = cv.Canny(img_blur, 55, 110)
        cv.imshow("canny", img_canny)

# kernel  = np.ones((3,3), np.uint8)
# img_dil = cv.dilate(img_canny, kernel, iterations=1)
# # img_ero = cv.erode(img_dil, kernel, iterations=1)
# closing = cv.morphologyEx(img_dil, cv.MORPH_CLOSE, kernel)
# cv.imshow("closing canny", closing)

if roi:
    roi = cv.selectROI("choose_region",img)
    y1 = int(roi[1])
    y2 = int(roi[1]+roi[3])
    x1 = int(roi[0])
    x2 = int(roi[0]+roi[2])
    img1 = img.copy()
    img_croped = img[y1:y2, x1:x2]
    cropped_th = th[y1:y2, x1:x2]

lines = cv.HoughLinesP(cropped_th,1,np.pi/180,100,800)


final_line = lines[len(lines)-1]
print(final_line)
for f in final_line:
    x1a = 0
    y1a = f[1]
    x2a = x2
    y2a = f[3]

line1 = cv.line(img_croped, (x1a,y1a), (x2a,y2a), (0,255,0), 2)
cv.imshow("line",line1)



cv.waitKey(0)