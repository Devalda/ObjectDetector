import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

path = "../images/micorlax_ex/mx2.jpg"
# path = "contour_1.png"
img = cv.imread(path)

lines = True
contours = True

image = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# convert to grayscale
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
gaus = cv.GaussianBlur(gray, (7, 7), 2)
ret, binary = cv.threshold(gaus, 80, 255, cv.THRESH_BINARY_INV)
kernel = np.ones((5, 5), np.uint8)
dilate = cv.dilate(binary, kernel, iterations=1)
cv.imshow("binary",dilate)

# line detect
# roi1 = cv.selectROI("select roi 1",img)
roi1 = (357, 763, 1771, 1236)
print("roi = ", roi1)
y1 = int(roi1[1])
y2 = int(roi1[1] + roi1[3])
x1 = int(roi1[0])
x2 = int(roi1[0] + roi1[2])
img1 = img.copy()
img_roi1 = dilate[y1:y2, x1:x2]
cropped1 = img[y1:y2, x1:x2]
cropped2 = img[y1:y2, x1:x2]
height, width, channels = img.shape
cropped_area = {'h':height,'w':width,'c':channels}
print(f"Croped_Area = height:{height} , width:{width}")

if lines :
    show_line = True
    height, width, channels = img.shape
    lines = cv.HoughLinesP(img_roi1, 1, np.pi / 180, 100,minLineLength=150)
    final_line = lines[len(lines) - 1]
    print("final_line", final_line)
    for f in final_line:
        x1L = 0
        y1L = f[1]
        x2L = width
        y2L = f[3]
    height, width = final_line.shape
    print("houghLines widht",width)
    line_above = cv.line(cropped1, (x1L, y1L), (x2L, y2L), (255, 0, 0), 2)
    boost = 200
    y1N = y1L + boost
    y2N = y2L + boost
    line_bottom = cv.line(cropped1, (x1L, y1N), (x2L, y2N), (255, 0, 0), 2)

    # region eyemark (vertical) from cropped ROI
    lines_above = {'hs': x1L, 'he': x2L, 'vs': y1L, 've': y2L}
    lines_bottom = {'hs': x1L, 'he': x2L, 'vs': y1L, 've': y2L}
    la = 've'
    lb = 've'
    print(f"above:{lines_above[la]} ,bottom{lines_bottom[lb]} ")
    # region eyemark (horizontal) cropped from vertical line detection
    lines_left = {'hs': 0, 'he': 0, 'vs': 0, 've': 0}
    lines_right = {'hs': 0, 'he': 0, 'vs': 0, 've': 0}

if contours:
    ###########################
    # canny_rectangle_cropper #
    ###########################

    edged = cv.Canny(img_roi1, 30, 200)
    contours, hierarchy = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        # the contours are drawn here
        cv.drawContours(cropped2, contours, -1, 255, 3)

        # find the biggest area of the contour
        c = max(contours, key=cv.contourArea)

        x, y, w, h = cv.boundingRect(c)
        # draw the 'human' contour (in green)
        cv.rectangle(cropped2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # finding width and length inside contour are
    xb, yb, wb, hb = cv.boundingRect(c)
    cv.imshow("img_contour",img)

    height, width, channels = img.shape
    print(f"contour_area = height:{height}, width:{width}")

    # todo:
    #  Documentation =
    #  Cont_Vertical_left      (CVL) || Cont_Vertical_right      (CVR)
    #  Cont_Horizontal_Above   (CHA) || Cont_Horizontal_Bottom   (CHB)
    #  Outline_Vertical_left   (OVL) || Outline_Vertical_rigth   (OVR)
    #  Outline_Horizontal_Above(OHA) || Outline_Horizontal_Bottom(OHB)


    OVL = 0
    OVR = cropped_area['w']
    OHA = 0
    OHB = cropped_area['h']
    CVR = xb+wb
    CVL = xb
    CHB = yb
    CHA = yb+hb

    a1  = OVR - CVR
    print(f"lebar crop:{OVR}, lebar cont:{wb}")

    a1a = int(wb/2)
    print("a1a",a1a)
    b1 = a1 - a1a
    print("lebar half cont", b1)

    c1 = CVR - a1a
    hh = int(hb/2)
    h1 = CHB + hh

    line_batas_kanan_h = cv.arrowedLine(cropped2,  (OVR, h1),(CVR, h1), (0,0,255), 5,tipLength = 0.03)
    line_batas_bawah_tengah = cv.arrowedLine(cropped2,  (c1, OHB),(c1, CHA), (0,0,255),5,tipLength = 0.03)

    line_batas_atas_tengah = cv.arrowedLine(cropped2,  (c1, 0),(c1, CHA-hb), (0,0,255),5,tipLength = 0.1)
    line_batas_kiri_h = cv.arrowedLine(cropped2, (0, h1), (CVR-wb, h1), (0, 0, 255), 5, tipLength=0.03)

    ## set the biggest contour(eyemark,not blob) us color ##
    # lower = [1, 0, 20]
    # upper = [60, 40, 220]
    # # create NumPy arrays from the boundaries
    # lower = np.array(lower, dtype="uint8")
    # upper = np.array(upper, dtype="uint8")
    # mask = cv.inRange(img, lower, upper)
    # output = cv.bitwise_and(cropped2, image, mask=mask)
    # ret, thresh = cv.threshold(mask, 40, 255, 0)

#Desicion Flow
cutoff = False

if CHB < y2N :
    print("reject - eyemark over pinched")
    cv.rectangle(cropped2, (x1L + 40 , y2L - 150), (x1L + 740, y2L - 50), (0, 0, 0), -1)
    cv.putText(cropped2, 'Eyemark OverPinched', (x1L + 50, y2L - 80), cv.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 6)
    cv.imshow("reject", cropped2)
elif cutoff:
    print("reject -- eyemark cutoff")
    cv.putText(cropped2, 'Eyemark CutOff', (x1L + 50, y2L - 80), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 6)
    cv.imshow("reject", cropped2)


cv.waitKey(0)
