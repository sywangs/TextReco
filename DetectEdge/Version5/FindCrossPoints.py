import math
import numpy as np
import cv2
import time

ERROR_NUM = -9999

Num = 0


def getCrossPoint(rho0,theta0,rho1,theta1):
    x0 = (rho1 * math.sin(theta0) - rho0 * math.sin(theta1))\
         / (math.sin(theta0) * math.cos(theta1) - math.sin(theta1) * math.cos(theta0))
    y0 = (rho0 * math.cos(theta1) - rho1 * math.cos(theta0)) \
         / (math.sin(theta0) * math.cos(theta1) - math.sin(theta1) * math.cos(theta0))
    return int(x0),int(y0)

def getPointsWithOutOrder(lines1,lines2,rows,cols):
    points = []

    for line in lines1:
        rho0 = line[0]
        theta0 = line[1]
        allCross = []
        for lineCross in lines2:
            rho1 = lineCross[0]
            theta1 = lineCross[1]
            x0,y0 = getCrossPoint(rho0,theta0,rho1,theta1)
            if x0 > 0 and x0 < cols and y0 > 0 and y0 < rows:
                allCross.append([x0,y0])
            else:
                allCross.append([ERROR_NUM,ERROR_NUM])

        points.append(allCross)

    rect = [[cols, rows], [0, rows],[0, 0], [cols, 0]]
    centerValue = 9999
    centerPos = (cols/2,rows/2)
    while len(points) > 0:
        allMainLinePoint = points.pop(0)

        while len(allMainLinePoint) > 0:
            mainPointMainLineNow = allMainLinePoint.pop(0)
            AllOtherTestPoints = np.array(allMainLinePoint).tolist()
            if mainPointMainLineNow == [ERROR_NUM,ERROR_NUM]:
                continue

            for testPointMainLine in AllOtherTestPoints:
                allOtherLines = np.array(points).tolist()
                if testPointMainLine == [ERROR_NUM, ERROR_NUM]:
                    continue

                while len(allOtherLines) > 0:
                    allTestLinePoint = allOtherLines.pop(0)
                    while len(allTestLinePoint) > 0:
                        mainPointTestLineNow = allTestLinePoint.pop(0)
                        if mainPointTestLineNow == [ERROR_NUM, ERROR_NUM]:
                            continue
                        for testPointTestLine in allTestLinePoint:
                            if testPointTestLine == [ERROR_NUM, ERROR_NUM]:
                                continue
                            centerValueNow = getCenterValue(mainPointMainLineNow,testPointMainLine, \
                                                       mainPointTestLineNow,testPointTestLine, \
                                                       centerPos)
                            if centerValueNow < centerValue:
                                rect = [mainPointMainLineNow,testPointMainLine,mainPointTestLineNow,testPointTestLine]
                                centerValue = centerValueNow
    rect = getRectWithOrder(rect)
    return rect

def getRectWithOrder(rect):
    rect.sort(key=lambda x:x[1],reverse=True)
    if rect[2][0] < rect[3][0]:
        p1 = rect[2]
        p2 = rect[3]
    else:
        p1 = rect[3]
        p2 = rect[2]

    if rect[0][0] < rect[1][0]:
        p3 = rect[1]
        p4 = rect[0]
    else:
        p3 = rect[0]
        p4 = rect[1]
    return [p1,p2,p3,p4]



def getCenterPos(p1,p2,p3,p4):
    x = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
    y = (p1[1] + p2[1] + p3[1] + p4[1]) / 4
    return x,y

def getCenterValue(p1,p2,p3,p4,centerPos):
    x, y = getCenterPos(p1, p2, p3, p4)

    lenthMain = math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
    lenthTest = math.sqrt((p4[1] - p3[1]) ** 2 + (p4[0] - p3[0]) ** 2)

    height13 = math.sqrt((p3[1] - p1[1]) ** 2 + (p3[0] - p1[0]) ** 2)
    height14 = math.sqrt((p4[1] - p1[1]) ** 2 + (p4[0] - p1[0]) ** 2)
    height23 = math.sqrt((p3[1] - p2[1]) ** 2 + (p3[0] - p2[0]) ** 2)
    height24 = math.sqrt((p4[1] - p2[1]) ** 2 + (p4[0] - p2[0]) ** 2)

    height = min(height13,height14,height23,height24)

    deltaX = math.fabs(p1[0]-x) + math.fabs(p2[0]-x) + math.fabs(p3[0]-x) + math.fabs(p4[0]-x)
    deltaY = math.fabs(p1[1]-y) + math.fabs(p2[1]-y) + math.fabs(p3[1]-y) + math.fabs(p4[1]-y)

    # print("------------------")
    # print("lenthMain > 200",lenthMain)
    # print("lenthTest > 200", lenthTest)
    # print("MinHeight > 200", height)
    # print("deltaX > 100", deltaX)
    # print("deltaY > 100", deltaY)
    # print("------------------")

    if lenthMain < 200 or lenthTest < 200 or height < 200 or deltaY < 100 or deltaX < 100:
        return 9999

    value =math.sqrt((centerPos[0] - x) ** 2 + (centerPos[1] - y) ** 2)
    # if value < 3:
    #     image = cv2.imread("/Users/developer/Documents/OCR/Correct/imageVersion5/testImage3.jpeg")
    #     rows, cols, chan = image.shape
    #     while rows > 1000 or cols > 1000:
    #         image = cv2.resize(image, (int(cols / 2), int(rows / 2)))
    #         rows, cols, chan = image.shape
    #
    #     pos1 = (p1[0],p1[1])
    #     pos2 = (p2[0],p2[1])
    #     pos3 = (p3[0],p3[1])
    #     pos4 = (p4[0],p4[1])
    #     cv2.putText(image, 'C1', pos1, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    #     cv2.putText(image, 'C2', pos2, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    #     cv2.putText(image, 'C3', pos3, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    #     cv2.putText(image, 'C4', pos4, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    #     cv2.putText(image,str(value),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        # cv2.putText(image,str(x) + ',' + str(y),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        # cv2.putText(image, str(int(cols/2)) +',' + str(int(rows/2)) + ':' + str(value),\
        #             (int(centerPos[0]),int(centerPos[1])), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        # cv2.putText(image, 'center', (int(centerPos[0]),int(centerPos[1])), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        # cv2.imwrite('./image/rectPoints' +str(time.time()) +'.jpg',image)
    # return value