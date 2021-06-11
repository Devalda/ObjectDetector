import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

path = "../images/micorlax_ex/mx2.jpg"
# path = "contour_1.png"
img = cv.imread(path)

lines = False
contours = False

image = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# convert to grayscale
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
ret, binary = cv.threshold(gray, 80, 255, cv.THRESH_BINARY_INV)

# line detect
# roi1 = cv.selectROI("select roi 1",img)
roi1 = (1628, 1028, 198, 229)
print("roi = ", roi1)
y1 = int(roi1[1])
y2 = int(roi1[1] + roi1[3])
x1 = int(roi1[0])
x2 = int(roi1[0] + roi1[2])
img1 = img.copy()
img_roi1 = binary[y1:y2, x1:x2]
cropped1 = img[y1:y2, x1:x2]
cropped2 = img[y1:y2, x1:x2]
height, width, channels = img.shape
cropped_area = {'h':height,'w':width,'c':channels}
print(f"Croped_Area = height:{height} , width:{width}")

if lines :
    show_line = True
    height, width, channels = img.shape
    lines = cv.HoughLinesP(img_roi1, 1, np.pi / 180, 100, 800)
    final_line = lines[len(lines) - 1]
    print("final_line", final_line)
    for f in final_line:
        x1a = 0
        y1a = f[1]
        x2a = width
        y2a = f[3]

    line_above = cv.line(cropped1, (x1a, y1a), (x2a, y2a), (255, 0, 0), 2)
    boost = 200
    y1b = y1a + boost
    y2b = y2a + boost
    line_bottom = cv.line(cropped1, (x1a, y1b), (x2a, y2b), (255, 0, 0), 2)

    if show_line:
        cv.imshow("check", line_bottom)

    # region eyemark (vertical) from cropped ROI
    lines_above = {'hs': x1a, 'he': x2a, 'vs': y1a, 've': y2a}
    lines_bottom = {'hs': x1a, 'he': x2a, 'vs': y1b, 've': y2b}
    a = 've'
    b = 've'
    print(f"above:{lines_above[a]} ,bottom{lines_bottom[b]} ")
    # region eyemark (horizontal) cropped from vertical line detection
    lines_left = {'hs': 0, 'he': 0, 'vs': 0, 've': 0}
    lines_right = {'hs': 0, 'he': 0, 'vs': 0, 've': 0}

if contours:
    ###########################
    # canny_rectangle_cropper #
    ###########################

    edged = cv.Canny(img_roi1, 30, 200)
    contours, hierarchy = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    print("no of shapes: {0}".format(len(contours)))
    for cnt in contours:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        img = cv.drawContours(cropped1, [box], 0, (0, 0, 255))  # BGR_Color_Sequence


    # finding width and length inside contour are
    xb, yb, wb, hb = cv.boundingRect(cnt)
    cv.imshow("img_contour",img)


    # finding center on detected shape
    for cnt in contours:
        M = cv.moments(cnt)
        print(f"Momen_Detected = m0:{M['m00']} , m10:{M['m10']} , m01:{M['m01']} ")

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0
        center = (cx, cy)
        print("Center coordinate: " + str(center))
        radius = 5
        cv.circle(img, (cx, cy), radius, (0, 255, 255), -1)

        epsilon = 0.01 * cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, epsilon, True)
        img = cv.drawContours(img, [approx], 0, (0, 255, 0), 2)
        cv.putText(img, "centroid", (cx - 20, cy - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv.imshow("contour", img)

    # are inside contour

    height, width, channels = img.shape
    print(f"contour_area = height:{height}, width:{width}")


    batas_outline_h_kiri = 0
    batas_outline_h_kanan = cropped_area['w']
    batas_outline_v_atas = 0
    batas_outline_v_bawah = cropped_area['h']
    titik_horizontal_kanan = xb+wb
    titik_horizontal_kiri = xb-wb
    titik_vertikal_atas = yb
    titik_vertikal_bawah = yb+hb

    a1  =batas_outline_h_kanan - titik_horizontal_kanan
    print(f"lebar crop:{batas_outline_h_kanan}, lebar cont:{wb}")

    a1a = int(wb/2)
    print("a1a",a1a)
    b1 = a1 - a1a
    print("lebar half cont", b1)

    c1 = titik_horizontal_kanan - a1a
    hh = int(hb/2)
    h1 = titik_vertikal_bawah - hh

    line_contour = cv.line(cropped2, (xb, yb), (xb + wb, yb + hb), (255, 0, 0), 2)
    line_batas_kanan = cv.line(cropped2, (titik_horizontal_kanan, xb), (batas_outline_h_kanan, xb), (255, 0, 0), 2)
    line_batas_kanan_h = cv.line(cropped2, (titik_horizontal_kanan, h1), (batas_outline_h_kanan, h1), (0,0,255), 2)
    line_batas_bawah = cv.line(cropped2, (titik_horizontal_kanan, titik_vertikal_bawah), (titik_horizontal_kanan, batas_outline_v_bawah), (255,0,0), 2)
    line_batas_bawah_tengah = cv.line(cropped2, (c1, titik_vertikal_bawah), (c1, batas_outline_v_bawah), (0,0,255), 2)
    cv.imshow("line batas",line_contour)


    ## set the biggest contour(eyemark,not blob) us color ##
    # lower = [1, 0, 20]
    # upper = [60, 40, 220]
    # # create NumPy arrays from the boundaries
    # lower = np.array(lower, dtype="uint8")
    # upper = np.array(upper, dtype="uint8")
    # mask = cv.inRange(img, lower, upper)
    # output = cv.bitwise_and(cropped2, image, mask=mask)
    # ret, thresh = cv.threshold(mask, 40, 255, 0)

cv.waitKey(0)
