## coding = utf-8
"""
this version is based on Canny and Houghlines
Find Cross Points of these lines
"""
import cv2
import math
import numpy as np

from DetectEdge.Version2.FindCrossPoints import getPointsWithOutOrder

ERROR_NUM = -9999

def DegreeTrans(avgAngle):
    angle = int(avgAngle / math.pi* 180)
    return angle

def ImageEdage(originInput):
    originInput = cv2.pyrMeanShiftFiltering(originInput, 25, 10)

    midImage = cv2.Canny(originInput,10,50,3)

    cv2.imwrite('./image/midImage.jpg',midImage)

    linesOri = cv2.HoughLines(midImage,1,math.pi/180,100,0,0)
    linesOri = linesOri.tolist()
    lines = []
    try:
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

            cv2.line(originInput,p1,p2,(0,0,255),5)

        cv2.imwrite('./image/houghlineImage.jpg', originInput)
        print("Edge detect success")
        return lines
    except:
        print("No edge in Image")

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
        # linesFinal = [lines[0]]
        # linesFinal.append(lines[-1])
        return lines
    else:
        return arr


def Main(imagePath,savePath):
    originInput = cv2.imread(imagePath)

    rows,cols,chan = originInput.shape
    print(rows,cols)
    while rows > 1000 or cols > 1000:
        originInput = cv2.resize(originInput, (int(cols / 2), int(rows / 2)))
        rows, cols, chan = originInput.shape

    edgeLines = ImageEdage(originInput)
    if len(edgeLines) > 0:
        lines1,lines2 = getCrossLines(edgeLines)
        points = getPointsWithOutOrder(lines1,lines2,rows,cols)

    pos1 = (points[0][0],points[0][1])
    pos2 = (points[1][0],points[1][1])
    pos3 = (points[2][0],points[2][1])
    pos4 = (points[3][0],points[3][1])
    cv2.putText(originInput, 'C1', pos1, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(originInput, 'C2', pos2, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(originInput, 'C3', pos3, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(originInput, 'C4', pos4, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(originInput,'cen',(int(cols/2),int(rows/2)),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.imwrite(savePath,originInput)

# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion1/testImage1.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion1/testImage2.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion1/testImage3.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion1/testImage4.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion1/testImage5.jpeg"
#
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion2/testImage1.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion2/testImage2.jpeg"
#
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion4/imageTest6.jpg"

# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImage1.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImage2.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImage3.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImage4.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImage5.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImage6.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImage7.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImage8.png"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImag3.png"
#

imagePath = "/Users/developer/Documents/OCR/Correct/imageVersionLeo/image2_leo.png"
savePath = "/Users/developer/Documents/OCR/Correct/imageVersionLeo/image2_result.png"

Main(imagePath,savePath)