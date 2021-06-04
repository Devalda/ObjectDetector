import imutils
import cv2
import matplotlib


# @@ rotated image
from imutils import contours
from matplotlib import pyplot as plt

image = "proris.png"
img = cv2.imread(image)

for angle in range(0, 360, 90):
	# rotate the image and display it
	rotated = imutils.rotate(img, angle=angle)
rotated = imutils.rotate(img, angle=170)
cv2.imshow(f"image: {image} || rotate : {angle}", rotated)


# @@ Resize Image, maintain aspect ratio
for width in (400, 300, 200, 100):
	# resize the image and display it
	resized = imutils.resize(img, width=width)
	cv2.imshow(f"resize image - width: {width}", resized)


# @@ skeletonize the image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
skeleton = imutils.skeletonize(gray, size=(3, 3))
cv2.imshow(f"Skeleton image : {image}", skeleton)


# @@ convert color - using matplotlib
plt.figure("before- plt imshow")
plt.imshow(img)

plt.figure("after- plt imshow imutils")
plt.imshow(imutils.opencv2matplotlib(img))
plt.show()


# @@ import image using url
url = "https://devalda.me/image.png"
image_url = imutils.url_to_image(url)
cv2.imshow("URL to Image", image_url)


# @@ Sorting Contours
orig = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edged = imutils.auto_canny(gray)

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the (unsorted) contours and label them
for (i, c) in enumerate(cnts):
	orig = contours.label_contour(orig, c, i, color=(240, 0, 159))

# show the original image
cv2.imshow("Original", orig)

# loop over the sorting methods
for method in ("left-to-right", "right-to-left", "top-to-bottom", "bottom-to-top"):
	# sort the contours
	(cnts, boundingBoxes) = contours.sort_contours(cnts, method=method)
	clone = image.copy()

	# loop over the sorted contours and label them
	for (i, c) in enumerate(cnts):
		sortedImage = contours.label_contour(clone, c, i, color=(240, 0, 159))

	# show the sorted contour image
	cv2.imshow(method, sortedImage)


# @@ (Recursively) Listing Paths to Images
from imutils import paths
for imagePath in paths.list_images("../object_measurment/img"):
	print (imagePath)


cv2.waitKey(0)

