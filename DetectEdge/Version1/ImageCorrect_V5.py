import cv2
import math
import sys
import os
import json

ERROR_NUM = -9999

def ImageRecify(image):
    originInput = image
    rows, cols, chan = originInput.shape

    while rows > 1000 or cols > 1000:
        originInput = cv2.resize(originInput, (int(cols / 2), int(rows / 2)))
        rows, cols, chan = originInput.shape

    gray = cv2.cvtColor(originInput, cv2.COLOR_RGB2GRAY)
    ret, binImage = cv2.threshold(gray, 150, 220, cv2.THRESH_BINARY)
    cv2.imwrite('./image/binImange.jpeg',binImage)

    result = [[cols, rows], [0, rows],[0, 0], [cols, 0]]

    _, countours, _ = cv2.findContours(binImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    i = 0
    for countour in countours:
        rect = cv2.minAreaRect(countour)
        rectpoint = cv2.boxPoints(rect)
        rectpoint = removeNegi(rectpoint)

        lenthLine1 = math.sqrt((rectpoint[1][1] - rectpoint[0][1]) ** 2 + (rectpoint[1][0] - rectpoint[0][0]) ** 2)
        lenthLine2 = math.sqrt((rectpoint[3][1] - rectpoint[0][1]) ** 2 + (rectpoint[3][0] - rectpoint[0][0]) ** 2)

        if (rows - lenthLine2 < 20 or cols - lenthLine1 < 20 or lenthLine1 * lenthLine2 < 6000):
            continue

        result = rectpoint

    for i in range(len(result)):
        result[i][0] = result[i][0] / cols
        result[i][1] = result[i][1] / rows

    pos1 = (int(result[0][0] * cols), int(result[0][1] * rows))
    pos2 = (int(result[1][0] * cols), int(result[1][1] * rows))
    pos3 = (int(result[2][0] * cols), int(result[2][1] * rows))
    pos4 = (int(result[3][0] * cols), int(result[3][1] * rows))

    cv2.putText(originInput, 'C1' + str(i), pos1, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(originInput, 'C2' + str(i), pos2, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(originInput, 'C3' + str(i), pos3, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(originInput, 'C4' + str(i), pos4, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    i = i + 1

    cv2.imwrite('/Users/developer/Documents/OCR/Correct/imageVersion5/imageCorp.jpeg',originInput)

    return result

def removeNegi(reactPoint):
    for i in range(len(reactPoint)):
        if reactPoint[i][0] < 0:
            reactPoint[i][0] = 0
        if reactPoint[i][1] < 0:
            reactPoint[i][1] = 1

    return  reactPoint


def getMinAndMaxPos(reactPoint):
    minx = 99999
    miny = 99999
    maxx = 0
    maxy = 0

    for item in reactPoint:
        if item[0] < minx:
            minx = item[0]
        if item[1] < miny:
            miny = item[1]

        if item[0] > maxx:
            maxx = item[0]
        if item[1] > maxy:
            maxy = item[1]

    return int(minx),int(miny),int(maxx),int(maxy)

if __name__ == "__main__":
    # argv = sys.argv
    imageURL = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImag3.png"
    # if len(argv) == 2 and os.path.exists(argv[1]):
    # imageURL = argv[1]
    image = cv2.imread(imageURL)
    rect = ImageRecify(image)
    result = {
        'success':0,
        'result':rect.tolist()
    }
    print(json.dumps(result))
    # else:
    #     result = {
    #         'success': 1,
    #         'result':[]
    #     }
    #     print(json.dumps(result))