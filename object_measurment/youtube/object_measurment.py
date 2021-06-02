import cv2
from object_measurment.youtube import utils

webcam = False

pathlib ='kertas.jpeg'
cap = cv2.VideoCapture(0)

# cap.set(id-param , measurment)
# brightnes
cap.set(10, 150)
# word
cap.set(3, 1920)
# height
cap.set(4, 1080)
# w paper
scale = 3
wP = 210 *scale
hP = 297 *scale

while True:

    if webcam:
        src , img = cap.read()
    else:
        img = cv2.imread(pathlib)
    # success , img = cap.read()

    img1 , conts = utils.getContours(img, minArea=50000, filter=4)

    if len(conts) != 0:
        biggets = conts[0][2]
        print(biggets)
        imgWarp = utils.warpImg(img, biggets, wP, hP)

        img2 , conts2 = utils.getContours(imgWarp, minArea=2000, filter=4, cThr=[50, 50], draw=False)
        # img2, conts2 = utils.getContours(img1 , showCanny=True)
        # cv2.imshow('canny=', img2)
        if len(conts) != 0:
            for obj in conts2:
                cv2.polylines(img2,[obj[2]],True,(0,255,0),2)
                nPoints = utils.reOrder(obj[2])
                nW = round((utils.findDis(nPoints[0][0] // scale, nPoints[1][0] // scale) / 10), 1)
                nH = round((utils.findDis(nPoints[0][0] // scale, nPoints[2][0] // scale) / 10), 1)

                cv2.arrowedLine(img2 , (nPoints[0][0][0],nPoints[0][0][1]),(nPoints[1][0][0],nPoints[1][0][1]),
                                (255,0,255), 3, 8, 0,0.05
                                )
                cv2.arrowedLine(img2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0],nPoints[2][0][1]),
                                (255, 0, 255), 3, 8,0,0.05
                                )
                x,y,w,h = obj[3]

                cv2.putText(img2 ,'{}cm'.format(nW),(x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2,)
                cv2.putText(img2, '{}cm'.format(nH), (x -70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX,1,(255, 0, 255), 2)
        cv2.imshow('a4', img2)

    img = cv2.resize(img1,(0,0),None, 0.5,0.5)
    cv2.imshow('test1' , img)
    cv2.waitKey(1000)
