import os
import cv2
import numpy as np
import utl as u
import glob

webcam = False

filename = '../R_1.png'

scale = 4
hP =210 *scale
wP = 297 *scale
asmo=[]
while True:
    if webcam:
        print("no")
    else:
        # img = u.load_images_from_folder(folder, filename)
        img = cv2.imread('R_1.png')
        # images = [cv2.imread(file) for file in glob.glob("../img/*.png")]
        # cv2.imshow('test', images)

    img1 , conts =u.getContours(img, minArea=300 , showCanny=True)
    asmo.append(1)
    print(f"conts{sum(asmo)}: ",conts)

    if len(conts) != 0:
        biggets = conts[0][2]
        imgWarp = u.warpImg(img , biggets, wP , hP)

        img2 , conts2  =u.getContours(imgWarp, minArea=1000 , filter=4 , cThr=[50,50],draw=False)

        # cv2.imshow('warpping', img2)

    print(f"object_refresh: {sum(asmo)}")
    img = cv2.resize(img1,(0,0),None, 0.5,0.5)
    # cv2.imshow('test1' , img)
    cv2.waitKey(1500)
