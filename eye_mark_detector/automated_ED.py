import sys
import cv2 as cv
import numpy as np
import copy
import matplotlib.pyplot as plt

def sort_contours(cnts, method="top-to-bottom"):
    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    boundingBoxes = [cv.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return (cnts, boundingBoxes)

cam = True
image = False

if cam:
    # cam = cv.VideoCapture(0)
    # cam.set(3, 1280)
    # cam.set(4, 720)(4, 720)
    # cam.set(10, 70)
    rois = []
    rois = [(555, 865, 1383, 396)]
    rois = [(555, 865, 1383, 396)]
    ed_std = []

    # only for test!!!
    images = {1: '../images/micorlax_ex/mx2.jpg', 2: '../images/micorlax_ex/mx_c1.jpg',
              3: '../images/micorlax_ex/mx_c2.jpg', 4: '../images/micorlax_ex/mx2_th2.jpg'}
    i = input("Select Image: ", )
    # img = cv.imread(images[int(i)])

    while True:
        try:
            lines = True
            contours = True
            color_line = (200, 0, 0)
            color_contour = (0,204,255)
            color_bbox = (0,255,0)

            # only for test!!!
            img = cv.imread(images[int(i)])
            # ret, img = cam.read()

            image = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            # convert to grayscale
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            gaus = cv.GaussianBlur(gray, (7, 7), 2)
            ret, binary = cv.threshold(gaus, 80, 255, cv.THRESH_BINARY_INV)
            kernel = np.ones((5, 5), np.uint8)
            dilate = cv.dilate(binary, kernel, iterations=1)

    # line detect

            if not rois:
                roi1 = cv.selectROI("select roi 1", img)
                rois.append(roi1)
            else:
                roi1 = rois[0]

            print("###########################################################")
            print("ROI = ", roi1)
            y1 = int(roi1[1])
            y2 = int(roi1[1] + roi1[3])
            x1 = int(roi1[0])
            x2 = int(roi1[0] + roi1[2])
            img1 = img.copy()
            img_roi1 = dilate[y1:y2, x1:x2]
            cropped1 = img[y1:y2, x1:x2]
            cropped2 = img[y1:y2, x1:x2]
            height, width, channels = img.shape
            cropped_area = {'h': height, 'w': width, 'c': channels}
            print(f"Croped_Area = height:{height} , width:{width}")

            # return if the object not ready
            if lines:
                show_line = True
                height, width, channels = img.shape
                lines = cv.HoughLinesP(img_roi1, 1, np.pi / 180, 100, minLineLength=150)
                final_line = lines[len(lines) - 1]
                print("selected line coordinate :", final_line)
                for x1, y1, x2, y2 in lines[0]:
                    x1L = x1
                    y1L = y1
                    x2L = x1 + 1250
                    y2L = y2
                x1L = x1L - 100
                x2L = x2L + 100
                boost = 200
                y1N = y1L + boost
                y2N = y2L + boost
                line_above = cv.line(cropped1, (x1L, y1L), (x2L, y2L), color_line , 3)
                line_bottom = cv.line(cropped1, (x1L, y1N), (x2L, y2N), color_line, 3)

                # region eyemark (vertical) from cropped ROI
                lines_above = {'hs': x1L, 'he': x2L, 'vs': y1L, 've': y2L}
                lines_bottom = {'hs': x1L, 'he': x2L, 'vs': y1L, 've': y2L}
                la = 've'
                lb = 've'
                print(f"lines_above:{lines_above[la]} ,lines_bottom:{lines_bottom[lb]} ")
                # region eyemark (horizontal) cropped from vertical line detection
                lines_left = {'hs': 0, 'he': 0, 'vs': 0, 've': 0}
                lines_right = {'hs': 0, 'he': 0, 'vs': 0, 've': 0}

            if contours:

                ###########################
                # canny_rectangle_cropper #
                ###########################

                edged = cv.Canny(img_roi1, 30, 200)
                contours, hierarchy = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

                # todo: ################# this is just for labeling || second contour  ##################

                if len(contours) != 0:
                    # // draw detected contour on area selected
                    cv.drawContours(cropped2, contours, -1, color_contour, 1)
                    # find the biggest area of the contour//eyemark
                    c = max(contours, key=cv.contourArea)

                    # print(f"C max value array : {c}")

                    x, y, w, h = cv.boundingRect(c)
                    print(f"CA for boundrect = x:{x} , y:{y} , w:{w} , h:{h}")
                    # draw the bbox contour on the biggest // eyemark
                    cv.rectangle(cropped2, (x, y), (x + w, y + h), (255,255,255), 3)

                # finding line on top
                cnts_line, boundingBoxes = sort_contours(contours, method="top-to-bottom")
                cnt = cnts_line[0]
                # finding line on top

                xb, yb, wb, hb = cv.boundingRect(c)
                xc, yc, wc, hc = cv.boundingRect(cnt)

                cv.rectangle(cropped1, (xb, yb), (xb + wb, yb + hb), (255, 255, 255), 5)
                cv.rectangle(cropped1, (xc, yc), (xc + wc, yc + hc), (255, 255, 0), 5)

                print(f"brect 1 = x:{xb} , y:{xb} , w:{wb} , h:{hb}")
                print(f"brect 2 = x:{xc} , y:{xc} , w:{wc} , h:{hc}")

                height, width, channels = img.shape

                #############################
                ####### width line range ####
                #############################
                s = round(width / 2)
                e = s + 10
                print(f"s:{s} , e:{e}")
                cv.line(cropped1, (s,10), (e,10), (255, 255, 0), 20)

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
            CVR = xb + wb
            CVL = xb
            CHB = yb
            CHA = yb + hb

            a1 = OVR - CVR
            print(f"lebar crop:{OVR}, lebar cont:{wb}")

            a1a = int(wb / 2)
            print("a1a", a1a)
            b1 = a1 - a1a
            print("lebar half cont", b1)

            c1 = CVR - a1a
            hh = int(hb / 2)
            h1 = CHB + hh

        # Arrow
            line_batas_kanan_h = cv.arrowedLine(cropped2, (OVR, h1), (CVR, h1), (0, 0, 255), 2, tipLength=0.03)
            line_batas_bawah_tengah = cv.arrowedLine(cropped2, (c1, OHB), (c1, CHA), (0, 0, 255), 2, tipLength=0.03)

            line_batas_atas_tengah = cv.arrowedLine(cropped2, (c1, 0), (c1, CHA - hb), (0, 0, 255), 2, tipLength=0.1)
            line_batas_kiri_h = cv.arrowedLine(cropped2, (0, h1), (CVR - wb, h1), (0, 0, 255), 2, tipLength=0.03)

        # Desicion Flow

            #console
            cutoff = False
            center_ROI = OVR / 2
            tolerate_range = 50

            if not ed_std:
                ed_std.append(hb)

            # eyemark_placement
            if CVR <= center_ROI + tolerate_range and CVR >= center_ROI - tolerate_range :
                print("EYEMARK ADA DI TENGAH astaga")
                cv.putText(cropped2, 'invalid eyemark placement', (x1L + 50, y2L - 80), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 6)
                cv.imshow("reject", cropped2)
            # eyemark_cutoff
            if CHB < y2N:
                print("reject - eyemark over pinched")
                cv.rectangle(cropped2, (x1L + 40, y2L - 150), (x1L + 740, y2L - 50), (0, 0, 0), -1)
                cv.putText(cropped2, 'Eyemark OverPinched', (x1L + 50, y2L - 80), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),6)
                cv.imshow("reject", cropped2)
            elif hb < ed_std[0]:
                print("reject -- eyemark cutoff")
                cv.putText(cropped2, 'Eyemark CutOff', (x1L + 50, y2L - 80), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 6)
                cv.imshow("reject", cropped2)

        except(AssertionError, TypeError, ZeroDivisionError, ValueError, NameError ):
            print(f"!! DATA FAILURE : {sys.exc_info()[0]} !!")
            if cv.waitKey(200) & 0xff == ord('q'):
                break
            continue

        cv.waitKey(200)
