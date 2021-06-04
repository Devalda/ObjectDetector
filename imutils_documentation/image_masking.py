import numpy as np
import argparse
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, default="proris.png",
	help="path to the input image")
args = vars(ap.parse_args())

# load the original input image and display it to our screen
image = cv2.imread(args["image"])
cv2.imshow("Original", image)

# mask only 2 pixel

mask = np.zeros(image.shape[:2], dtype="uint8")
cv2.rectangle(mask, (0, 90), (290, 450), 255, -1)
cv2.imshow("Rectangular Mask", mask)
# apply our mask -- notice how only the person in the image is
# cropped out
masked = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Mask Applied to Image", masked)
cv2.waitKey(0)

