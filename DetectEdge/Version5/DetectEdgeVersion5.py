## coding = utf-8
"""
this version is based on Canny and Houghlines
Find Cross Points of these lines
"""
import cv2
import math
import numpy as np
import os
import sys
import time
import json

from FindCrossPoints import getPointsWithOutOrder

ERROR_NUM = -9999

def DegreeTrans(avgAngle):
    angle = int(avgAngle / math.pi* 180)
    return angle

def ImageEdage(originInput,savePath):
    # originInput = cv2.pyrMeanShiftFiltering(originInput, 25, 10)

    midImage = cv2.Canny(originInput,10,50,3)

    cv2.imwrite('./image/midImage.jpg',midImage)

    linesOri = cv2.HoughLines(midImage,1,math.pi/180,50,0,0)

    try:
        linesOri = linesOri.tolist()
        lines = []
        while True:
            if len(linesOri) == 0:
                break
            item = linesOri.pop(0)
            rhoMain = item[0][0]
            thetaMain = item[0][1]
            lines.append([rhoMain,thetaMain])

            if len(linesOri) == 0:
                break


            for other in linesOri:
                rhoGuest = other[0][0]
                thetaGuest = other[0][1]

                isClose1 = math.fabs(rhoMain - rhoGuest) + \
                          math.fabs(thetaMain - thetaGuest) * 100

                if isClose1 < 170:
                    linesOri.remove(other)
        for item in lines:
            rho = item[0]
            theta = item[1]
        #
            cosValue = math.cos(theta)
            sinValue = math.sin(theta)
        #
            x0 = cosValue * rho
            y0 = sinValue * rho

            x1 = int(round(x0 + 1000 * (-sinValue)))
            y1 = int(round(y0 + 1000 * cosValue))

            x2 = int(round(x0 - 1000 * (-sinValue)))
            y2 = int(round(y0 - 1000 * cosValue))

            p1 = (x1,y1)
            p2 = (x2,y2)

            cv2.line(originInput,p1,p2,(255,255,255),5)
        #
        # cv2.imwrite(savePath, originInput)
        print("Edge detect success")
        return lines
    except:
        print("No edge in Image")
        return[]

def getCrossLines(edgeLines):
    lines1 = []
    lines2 = []

    lineRoot = edgeLines.pop(0)
    lines1.append(lineRoot)
    thetaRoot = lineRoot[1]

    while len(edgeLines) > 0:
        lineCheck = edgeLines.pop(0)
        thetaCheck = lineCheck[1]

        isOneClass = math.fabs(thetaRoot - thetaCheck)

        if isOneClass > (math.pi/2):
            isOneClass = math.pi - isOneClass

        if isOneClass < 0.2:
            lines1.append(lineCheck)
        else:
            lines2.append(lineCheck)

    lines1 = sortArray(lines1)
    lines2 = sortArray(lines2)

    return lines1,lines2

def sortArray(arr):
    if len(arr) > 1:
        lines= np.array(arr)
        lines = lines[lines[:,0].argsort()].tolist()
        return lines
    else:
        return arr

def getOrderedPoints(srcTi):

    arr = np.float32(srcTi)
    seq = arr[:,1].argsort()

    t1 = seq.tolist()[0]
    t2 = seq.tolist()[1]
    result = []
    if arr[t1][0] < arr[t2][0]:
        min = t1
    else:
        min = t2

    for i in range(4):
        result.append(srcTi[(min + i) % 4])
    return np.float32(result)


def Main(imagePath,savePath):
    originInput = cv2.imread(imagePath)

    rows,cols,chans = originInput.shape
    # print(rows,cols)

    while rows < 1000 or cols < 1000:
        originInput = cv2.resize(originInput, (int(cols * 2), int(rows * 2)))
        rows, cols, chan = originInput.shape

    while rows > 1000 or cols > 1000:
        originInput = cv2.resize(originInput, (int(cols / 2), int(rows / 2)))
        rows, cols, chan = originInput.shape

    (B, G, R) = cv2.split(originInput)
    B = cv2.GaussianBlur(B, (5, 5), 10)

    ret, th = cv2.threshold(B, 0, 255, cv2.THRESH_OTSU)

    g = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    img_open = cv2.morphologyEx(th, cv2.MORPH_CLOSE, g)

    edgeLines = ImageEdage(img_open,savePath)
    if len(edgeLines) > 0:
        lines1,lines2 = getCrossLines(edgeLines)
        pointsNeed = getPointsWithOutOrder(lines1,lines2,rows,cols)

        # pos1 = (pointsNeed[0][0],pointsNeed[0][1])
        # pos2 = (pointsNeed[1][0],pointsNeed[1][1])
        # pos3 = (pointsNeed[2][0],pointsNeed[2][1])
        # pos4 = (pointsNeed[3][0],pointsNeed[3][1])
        # cv2.putText(originInput, 'C1', pos1, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        # cv2.putText(originInput, 'C2', pos2, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        # cv2.putText(originInput, 'C3', pos3, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        # cv2.putText(originInput, 'C4', pos4, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        # cv2.putText(originInput,'cen',(int(cols/2),int(rows/2)),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        # cv2.imwrite(savePath,originInput)

        pointsNeed = getOrderedPoints(pointsNeed)

        pointsNeed = [
            [pointsNeed[0][0] / cols, pointsNeed[0][1] /rows],
            [pointsNeed[1][0] / cols, pointsNeed[1][1] / rows],
            [pointsNeed[2][0] / cols, pointsNeed[2][1] / rows],
            [pointsNeed[3][0] / cols, pointsNeed[3][1] / rows]
        ]

        return pointsNeed


if __name__ == "__main__":
    argv = sys.argv
    start = time.time()
    # imageURL = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImage8.png"
    if len(argv) == 2 and os.path.exists(argv[1]):
        imageURL = argv[1]
        # image = cv2.imread(imageURL)
        rect = Main(imageURL, imageURL.split("/")[-1])
        result = {
            'success': 0,
            'result': rect
        }
        print(json.dumps(result))
    else:
        result = {
            'success': 1,
            'result': []
        }
        print(json.dumps(result))
    # print('total Time :' + str(time.time() - start))

# imgpath = "/Users/developer/Downloads/image/56.jpg"
# savePath = './image/save.jpg'
# Main(imgpath,savePath)

# imgType = ['jpeg','jpg','png']
# for root, dirs, files in os.walk("/Users/developer/Downloads/", topdown=False):
#     for name in dirs:
#         imageDir = os.path.join(root,name)
#         for filePath in os.listdir(imageDir):
#             if filePath.split('.')[-1] in imgType:
#                 imgpath = os.path.join(imageDir,filePath)
#                 savePath = os.path.join(imageDir,'cropPos' + filePath)
#                 Main(imgpath,savePath)

# for root, dirs, files in os.walk("/Users/developer/PycharmProjects/TextReco/", topdown=False):
#     for name in dirs:
#         imageDir = os.path.join(root,name)
#         for filePath in os.listdir(imageDir):
#             if filePath.split('.')[-1] in imgType:
#                 imgpath = os.path.join(imageDir,filePath)
#                 savePath = os.path.join(imageDir,'cropPos' + filePath)
#                 Main(imgpath,savePath)