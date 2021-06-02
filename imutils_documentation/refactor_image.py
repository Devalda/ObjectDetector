import imutils
import cv2
import matplotlib


#  rotated image
from matplotlib import pyplot as plt

image = "proris.png"
img = cv2.imread(image)

for angle in range(0, 360, 90):
	# rotate the image and display it
	rotated = imutils.rotate(img, angle=angle)
rotated = imutils.rotate(img, angle=170)
cv2.imshow(f"image: {image} || rotate : {angle}", rotated)


# Resize Image, maintain aspect ratio
for width in (400, 300, 200, 100):
	# resize the image and display it
	resized = imutils.resize(img, width=width)
	cv2.imshow(f"resize image - width: {width}", resized)


# skeletonize the image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
skeleton = imutils.skeletonize(gray, size=(3, 3))
cv2.imshow(f"Skeleton image : {image}", skeleton)


# convert color - using matplotlib
plt.figure("before- plt imshow")
plt.imshow(img)

plt.figure("after- plt imshow imutils")
plt.imshow(imutils.opencv2matplotlib(img))
plt.show()


# import image using url
url = "https://devalda.me/image.png"
image_url = imutils.url_to_image(url)
cv2.imshow("URL to Image", image_url)


cv2.waitKey(0)