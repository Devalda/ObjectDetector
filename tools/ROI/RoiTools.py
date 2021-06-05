import cv2
import numpy as np

class select_roi():

    def select_roi_solo(image):
        # img_path= image
        # img_raw = cv2.imread(img_path)

        #select ROI function
        roi = cv2.selectROI(image)
        print(roi)

        #Crop selected roi from raw image
        roi_cropped = image[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        cv2.imshow("ROI", roi_cropped)
        return roi

    def select_roi_group(image):

        img_path = image
        img_raw = cv2.imread(img_path)

        # select ROIs function
        ROIs = cv2.selectROIs("Select Rois", img_raw)
        print(ROIs)

        # counter to save image with different name
        crop_number = 0

        # loop over every bounding box save in array "ROIs"
        for rect in ROIs:
            x1 = rect[0]
            y1 = rect[1]
            x2 = rect[2]
            y2 = rect[3]

            # crop roi from original image
            img_crop = img_raw[y1:y1 + y2, x1:x1 + x2]

            # show cropped image
            cv2.imshow("crop" + str(crop_number), img_crop)

            # save cropped image
            roi =  cv2.imwrite("crop" + str(crop_number) + ".jpeg", img_crop)

            crop_number += 1

        return roi
