# coding = utf-8

'''
call example：
python DetectEdge/Version4/DetectEdgeVersion4_test.py /Users/developer/Documents/OCR/Correct/imageVersion5/testImage7.jpeg
return result:
success:
{
    "result": [[0.14074073731899261, 0.918055534362793], [0.14074073731899261, 0.1180555522441864], [0.8425925970077515, 0.1180555522441864], [0.8425925970077515, 0.918055534362793]],
    "success": 0
}
fail:
{
    'success': 1,
    'result':[]
}
'''

import cv2
import os
import sys
import math
import json
import time


def reverse(image):
    image2 = image.copy()
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            image2[i, j] = 255 - image[i, j]
    return image2


def getRect(image, filename):
    rows, cols = image.shape

    _, countours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    AreaNow = 0
    rectNow = [[cols, rows], [0, rows], [0, 0], [cols, 0]]

    # i = 0
    for countour in countours:
        rect = cv2.minAreaRect(countour)
        rectpoint = cv2.boxPoints(rect)

        out = removeNegi(rectpoint, rows, cols)
        if out:
            continue

        lenthLine1 = math.sqrt((rectpoint[1][1] - rectpoint[0][1]) ** 2 + (rectpoint[1][0] - rectpoint[0][0]) ** 2)
        lenthLine2 = math.sqrt((rectpoint[3][1] - rectpoint[0][1]) ** 2 + (rectpoint[3][0] - rectpoint[0][0]) ** 2)

        if rows - lenthLine1 < 20 \
                or cols - lenthLine2 < 20 \
                or lenthLine1 < 20 \
                or lenthLine2 < 20 \
                or lenthLine1 * lenthLine2 < AreaNow:
            continue
        AreaNow = lenthLine1 * lenthLine2
        rectNow = getNormal(rectpoint, cols, rows)

    return rectNow


def getNormal(rectpoint, cols, rows):
    for i in range(len(rectpoint)):
        rectpoint[i][0] = rectpoint[i][0] / cols
        rectpoint[i][1] = rectpoint[i][1] / rows
    return rectpoint.tolist()


def removeNegi(reactPoint, rows, cols):
    out = False
    for i in range(len(reactPoint)):
        if reactPoint[i][0] <= 0 or reactPoint[i][0] >= cols or reactPoint[i][1] <= 0 or reactPoint[i][1] >= rows:
            out = True
    return out


def ImageRecify(image, filename):
    rows, cols, chan = image.shape
    while rows > 1000 or cols > 1000:
        image = cv2.resize(image, (int(cols / 2), int(rows / 2)))
        rows, cols, chan = image.shape

    (B, G, R) = cv2.split(image)
    B = cv2.GaussianBlur(B, (5, 5), 10)

    ret, th = cv2.threshold(B, 0, 255, cv2.THRESH_OTSU)

    g = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    img_open = cv2.morphologyEx(th, cv2.MORPH_CLOSE, g)

    rect = getRect(reverse(img_open), filename)
    return rect


if __name__ == "__main__":
    argv = sys.argv
    start = time.time()
    # imageURL = "/Users/developer/Documents/OCR/Correct/imageVersion5/testImage8.png"
    if len(argv) == 2 and os.path.exists(argv[1]):
        imageURL = argv[1]
        image = cv2.imread(imageURL)
        rect = ImageRecify(image, imageURL.split("/")[-1])
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
    print('total Time :' + str(time.time() - start))

