## this version I am going to try to detect the angle by lines angle
import cv2
import math
import numpy as np

from DetectEdge.Version2.FindCrossPoints import getPointsWithOutOrder

ERROR_NUM = -9999

def DegreeTrans(avgAngle):
    angle = int(avgAngle / math.pi* 180)
    return angle

def ImageEdage(originInput,rows, cols):
    midImage = cv2.Canny(originInput,10,50,3)

    cv2.imwrite('./image/midImage.jpg',midImage)

    linesOri = cv2.HoughLines(midImage,1,math.pi/180,150,0,0)
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

        x0 = cosValue * rho
        y0 = sinValue * rho

        x1 = int(round(x0 + 1000 * (-sinValue)))
        y1 = int(round(y0 + 1000 * cosValue))

        x2 = int(round(x0 - 1000 * (-sinValue)))
        y2 = int(round(y0 - 1000 * cosValue))

        p1 = (x1,y1)
        p2 = (x2,y2)

        cv2.line(originInput,p1,p2,(255,255,255),5)


    image = getPureEdgeImage(originInput)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ret, binImage = cv2.threshold(gray, 150, 200, cv2.THRESH_BINARY)
    _, countours, _ = cv2.findContours(binImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    cv2.imwrite('./image/houghlineImage.jpg', originInput)
    cv2.imwrite('./image/PureEdge.jpg', image)

    AreaNow = 0
    rectNow =  [[cols, rows], [0, rows],[0, 0], [cols, 0]]

    i = 0
    for countour in countours:
        rect = cv2.minAreaRect(countour)
        rectpoint = cv2.boxPoints(rect)

        out = removeNegi(rectpoint,rows,cols)
        if out:
            continue

        lenthLine1 = math.sqrt((rectpoint[1][1] - rectpoint[0][1]) ** 2 + (rectpoint[1][0] - rectpoint[0][0]) ** 2)
        lenthLine2 = math.sqrt((rectpoint[3][1] - rectpoint[0][1]) ** 2 + (rectpoint[3][0] - rectpoint[0][0]) ** 2)

        if rows - lenthLine1 < 20 \
                or cols - lenthLine2< 20 \
                or lenthLine1 < 20 \
                or lenthLine2 < 20 \
                or  lenthLine1 * lenthLine2 < AreaNow:
            continue
        AreaNow = lenthLine1 * lenthLine2

        pos1 = (rectpoint[0][0],rectpoint[0][1])
        pos2 = (rectpoint[1][0],rectpoint[1][1])
        pos3 = (rectpoint[2][0],rectpoint[2][1])
        pos4 = (rectpoint[3][0],rectpoint[3][1])
        cv2.putText(image, 'C1' + str(i), pos1, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(image, 'C2' + str(i), pos2, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(image, 'C3' + str(i), pos3, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(image, 'C4' + str(i), pos4, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        cv2.imwrite('./Users/developer/Documents/OCR/Correct/imageVersion5/imageCorpVersion3.jpeg', image)

        rectNow = [pos1,pos2,pos3,pos4]
        i = i + 1
    # pos1 = rectNow[0]
    # pos2 = rectNow[1]
    # pos3 = rectNow[2]
    # pos4 = rectNow[3]
    # cv2.putText(originInput, 'C1' + str(i), pos1, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    # cv2.putText(originInput, 'C2' + str(i), pos2, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    # cv2.putText(originInput, 'C3' + str(i), pos3, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    # cv2.putText(originInput, 'C4' + str(i), pos4, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    # cv2.imwrite('/Users/developer/Documents/OCR/Correct/imageVersion5/imageCorpVersion3.jpeg', originInput)
    print("Edge detect success")
    return rectNow

def removeNegi(reactPoint,rows,cols):
    out = False
    for i in range(len(reactPoint)):
        if reactPoint[i][0] <= 0 or reactPoint[i][0] >=cols or reactPoint[i][1] <= 0 or reactPoint[i][1] >=rows:
            out = True

    return  out

def getPureEdgeImage(image):

    height, width, temp = image.shape
    img2 = image.copy()

    for i in range(height):
        for j in range(width):
            if not img2[i,j].tolist() == [255,255,255]:
                img2[i, j] = (0,0,0)
    return img2

def Main(imagePath):
    originInput = cv2.imread(imagePath)

    rows,cols,chan = originInput.shape
    print(rows,cols)
    while rows > 1000 or cols > 1000:
        originInput = cv2.resize(originInput, (int(cols / 2), int(rows / 2)))
        rows, cols, chan = originInput.shape

    points = ImageEdage(originInput,rows, cols)


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
#
imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImag3.png"

Main(imagePath)