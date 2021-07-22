import cv2 as cv
import numpy as np

def print2largest(arr, arr_size):
    # There should be atleast
    # two elements
    if (arr_size < 2):
        print(" Invalid Input ");
        return;

    largest = second = -2454635434;
    # Find the largest element
    for i in range(0, arr_size):
        largest = max(largest, arr[i]);

    # Find the second largest element
    for i in range(0, arr_size):
        if (arr[i] != largest):
            second = max(second, arr[i]);

    if (second == -2454635434):
        print("There is no second " +
              "largest element");
    else:
        print("The second largest " +
              "element is \n", second);

#################################################################################

img = cv.imread('../images/micorlax_ex/mx2.jpg')
image = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# convert to grayscale
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
gaus = cv.GaussianBlur(gray, (7, 7), 2)
ret, binary = cv.threshold(gaus, 80, 255, cv.THRESH_BINARY_INV)
kernel = np.ones((5, 5), np.uint8)
dilate = cv.dilate(binary, kernel, iterations=1)

roi1 = (555, 865, 1383, 396)
y1 = int(roi1[1])
y2 = int(roi1[1] + roi1[3])
x1 = int(roi1[0])
x2 = int(roi1[0] + roi1[2])
img1 = img.copy()
img_roi1 = dilate[y1:y2, x1:x2]
cropped1 = img[y1:y2, x1:x2]
cropped2 = img[y1:y2, x1:x2]
cropped3 = img[y1:y2, x1:x2]
height, width, channels = img.shape
cropped_area = {'h': height, 'w': width, 'c': channels}


edged = cv.Canny(img_roi1, 30, 200)
contours, hierarchy = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

areas = [cv.contourArea(c) for c in contours]
max_index = np.argmax(areas)
print(f"max index : {max_index}")
cnt=contours[7]
print(f"print max contours : {cnt}")
x, y, w, h = cv.boundingRect(cnt)


center  = round(h/2)
cv.rectangle(img , (center,center) , (center+2,center+2) , (255,255,0),5)

print(f"CA for boundrect = x:{x} , y:{y} , w:{w} , h:{h}")
cv.rectangle(cropped2, (x, y), (x + w, y + h), (255,255,255), 5)

# index ke enam merupakan contour yang terpanjang pada garis akhir: penyebab(belum tau )

sort = sorted(contours, key=cv.contourArea)

n = len(contours)
arr = contours.sort

# print(f"contour sorted lambda : {sorted_array}")

# print2largest(contours, n);f

image_contour = cropped1
cv.drawContours(image_contour, contours, -1, (200, 255, 0), 1)
cv.imshow("the longest contour", image_contour)
cv.waitKey(0)