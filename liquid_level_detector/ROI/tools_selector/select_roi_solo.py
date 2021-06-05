import cv2
import numpy as np

class roi_solo():

    def select_roi(image):
        img_path= image
        img_raw = cv2.imread(img_path)

        #select ROI function
        roi = cv2.selectROI(img_raw)
        print(roi)

        #Crop selected roi from raw image
        roi_cropped = img_raw[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

        cv2.imshow("ROI", roi_cropped)

        cv2.imwrite("../crop.jpeg", roi_cropped)

        return roi