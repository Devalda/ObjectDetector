import cv2
import numpy as np 

def getContours(img, cThr=[100,100] , showCanny=False , minArea = 1000 , filter = 0 , draw=False):
    imgGray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray , (1,3) , 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0],cThr[1])
    kernel = np.ones((1,1))
    imgDial = cv2.dilate(imgCanny , kernel, iterations=3)
    imgThres = cv2.erode(imgDial , kernel , iterations=2)
    if showCanny:
        cv2.imshow('Canny' , imgThres)

    contours , hiearchy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            par = cv2.arcLength(i,True)
            # 0.02 *  parlengt : find epsilon value
            approx = cv2.approxPolyDP(i,0.02*par,True)
            bbox = cv2.boundingRect(approx)
            if filter > 0 :
                if len(approx) == filter:
                    finalCountours.append([len(approx), area, approx, bbox, i])
            else:
                finalCountours.append([len(approx), area, approx, bbox, i])

    finalCountours = sorted(finalCountours,key=lambda x:x[1],reverse=True)
    if draw:
        for con in finalCountours:
            cv2.drawContours(img,con[4],-1,(0,0,225),3)
    return img , finalCountours


# set points on dis funtion -set micorlax points
def reOrder(myPoints):
    print("point_shape: ",myPoints.shape)
    myPointsN = np.zeros_like(myPoints)
    myPoints = myPoints.reshape((4,2))
    add = myPoints.sum(1)
    myPointsN[0] = myPoints[np.argmin(add)]
    myPointsN[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints,axis=1)
    myPointsN[1]=myPoints[np.argmin(diff)]
    myPointsN[2] = myPoints[np.argmax(diff)]
    return myPointsN

def warpImg(img , points , w , h,pad=20):
    # print("points: ",points)
    points= reOrder(points)
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    matrix = cv2.getPerspectiveTransform(pts1 , pts2)
    imgWarp = cv2.warpPerspective(img ,matrix,(w,h))
    imgWarp = imgWarp[pad:img.shape[0]-pad,pad:imgWarp.shape[1]-pad]
    return imgWarp

def findDis(pts1 , pts2):
    return((pts2[0]-pts1[0])**2 + (pts2[1]-pts1[1])**2)**0.5
