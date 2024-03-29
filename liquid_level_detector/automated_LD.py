import cv2 as cv
from numpy.lib import math
import numpy as np
import sys
from tools.ROI.RoiTools import select_roi

# spek botol
# tinggi botol : 9,8 cm || jarak leher botol(boddy-head): 2cm || lebar body : 3cm || lebar leher : 1cm

image = False
cam = True

if cam:
    # cam
    cam = cv.VideoCapture(0)
    cam.set(3, 1280)
    cam.set(4, 720)
    cam.set(10, 70)
    rois = []
    while True :

        try :
            # test for exeption handling
            # path = "../images/proris_new/p3.png"
            # img = cv.imread(path)

            ret , img = cam.read()
            cv.imshow("cam",img)

            if not rois:
                roi = cv.selectROI("select roi 1", img)
                rois.append(roi)
            else:
                roi = rois[0]


            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            img_blur = cv.GaussianBlur(img_gray, (7, 7), 2)
            ret, th = cv.threshold(img_blur, 0, 255, cv.THRESH_OTSU)
            img_canny = cv.Canny(th, 55, 110)

            # closed line
            kernel = np.ones((5, 5), np.uint8)
            img_dil = cv.dilate(img_canny, kernel, iterations=1)
            img_ero = cv.erode(img_dil, kernel, iterations=1)
            closing = cv.morphologyEx(img_dil, cv.MORPH_CLOSE, kernel)

            #roi
            # roi = (354, 730, 252, 280)
            y1 = int(roi[1])
            y2 = int(roi[1] + roi[3])
            x1 = int(roi[0])
            x2 = int(roi[0] + roi[2])
            img1 = img.copy()
            img_roi = closing[y1:y2, x1:x2]
            cropped = img[y1:y2, x1:x2]

            # set line inside roi
            minLineLength = 800
            maxLineGap = 10
            lines = cv.HoughLinesP(img_roi, 1, np.pi / 180, 100, minLineLength)

            final_line = lines[len(lines) - 1]
            print(final_line)
            for f in final_line:
                x1a = 0
                y1a = f[1]
                x2a = x2
                y2a = f[3]

            line = cv.line(cropped, (x1a, y1a), (x2a, y2a), (255, 0, 0), 2)
            cv.imshow("line", line)

        # return if the object not ready
        except(AssertionError,TypeError ,ZeroDivisionError ,ValueError ):
            print(f"!! No Data Detected : {sys.exc_info()[0]} !!")
            if cv.waitKey(1) & 0xff == ord('q'):
                break
            continue


        # create calculation and add standar deviation
        height, width, channels = cropped.shape
        mean = height / 2
        batas_of = mean - 20
        batas_uf = mean + 20

        print("mean : ", mean, " y2a: ", y2a)

        # add statement and create boundingbox decision
        if y2a == mean:
            bbox1 = cv.rectangle(img1, (x1, y1), (x2, y2), (0, 255, 0), 5)
            cv.putText(bbox1, 'Perfect', (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv.imshow("Decision Box", bbox1)

        elif y2a < batas_of:
            bbox1 = cv.rectangle(img1, (x1, y1), (x2, y2), (255, 0, 0), 5)
            cv.putText(bbox1, 'OverFilled', (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv.imshow("Decision Box", bbox1)

        elif y2a > batas_uf:
            bbox1 = cv.rectangle(img1, (x1, y1), (x2, y2), (0, 0, 255), 5)
            cv.putText(bbox1, 'UnderFilled', (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv.imshow("Decision Box", bbox1)

        else:
            bbox1 = cv.rectangle(img1, (x1, y1), (x2, y2), (0, 255, 0), 5)
            cv.putText(bbox1, 'within target', (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv.imshow("Decision Box", bbox1)

        if cv.waitKey(1) & 0xff == ord('q'):
            print("--end--of--the--session--")
            break


if image :

    # image
    path = "../images/proris_new/p3.png"
    img = cv.imread(path)
    img_gray    = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_blur    = cv.GaussianBlur(img_gray, (7, 7), 2)
    ret, th = cv.threshold(img_blur, 0, 255, cv.THRESH_OTSU)
    img_canny   = cv.Canny(th, 55,110)

    # closed line
    kernel  = np.ones((5,5), np.uint8)
    img_dil = cv.dilate(img_canny, kernel, iterations=1)
    img_ero = cv.erode(img_dil, kernel, iterations=1)
    closing = cv.morphologyEx(img_dil, cv.MORPH_CLOSE, kernel)
    while True :
        try:
            # define roi1
            roi1 = cv.selectROI("select roi 1",img)
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
            lines = cv.HoughLinesP(img_roi1,1,np.pi/180,100,minLineLength)


            final_line = lines[len(lines)-1]
            print(final_line)
            for f in final_line:
                x1a = 0
                y1a = f[1]
                x2a = x2
                y2a = f[3]

            line1 = cv.line(cropped1, (x1a,y1a), (x2a,y2a), (255,0,0), 2)
            cv.imshow("line",line1)
        except(TypeError):
            print("line not detected")
            continue

        # set average_indicator for liquid [within target , overfilled , underfilled]
            # todo : (wt = within target , of = overfilled , uf = underfilled)

        wt = ''
        of = ''
        uf = ''

        # create calculation and add standar deviation
        height, width, channels = cropped1.shape
        mean = height/2
        batas_of = mean - 20
        batas_uf = mean + 20

        print("mean : ",mean , " y2a: ",y2a)

        # add statement and create boundingbox decision
        if y2a == mean:
            bbox1 = cv.rectangle(img1, (x1, y1), (x2, y2), (0,255,0), 5)
            cv.putText(bbox1, 'Perfect', (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv.imshow("Decision Box",bbox1)

        elif y2a < batas_of:
            bbox1 = cv.rectangle(img1, (x1, y1), (x2, y2), (255,0,0), 5)
            cv.putText(bbox1, 'OverFilled', (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv.imshow("Decision Box",bbox1)

        elif y2a > batas_uf:
            bbox1 = cv.rectangle(img1, (x1, y1), (x2, y2), (0, 0, 255), 5)
            cv.putText(bbox1, 'UnderFilled', (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv.imshow("Decision Box",bbox1)

        else:
            bbox1 = cv.rectangle(img1, (x1, y1), (x2, y2), (0,255,0), 5)
            cv.putText(bbox1, 'within target', (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv.imshow("Decision Box",bbox1)

        if (cv.waitKey(1) & 0xFF) == ord('q'):
            break

    cv.waitKey(0)




