# -*- coding:utf-8 -*-
import sys,os
sys.path.append("../../../")

import cv2
import numpy as np

import math

# from DetectEdgeVersion4_test import ImageRecify
from DetectEdgeVersion5 import Main

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

def getMaxWH(rect):
    pos1 = rect[0]
    pos2 = rect[1]
    pos3 = rect[2]
    pos4 = rect[3]

    width1 = math.sqrt( (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 )
    width2 = math.sqrt((pos4[0] - pos3[0]) ** 2 + (pos4[1] - pos3[1]) ** 2)

    height1 = math.sqrt( (pos1[0] - pos4[0])**2 + (pos1[1] - pos4[1])**2 )
    height2 = math.sqrt( (pos2[0] - pos3[0])**2 + (pos2[1] - pos3[1])**2 )

    widthMax = max(width1,width2)
    heightMax = max(height1,height2)

    return int(widthMax),int(heightMax)

def getCovertedImage(Img,srcTi):
    SrcPoints = getOrderedPoints(srcTi)

    cols,rows = getMaxWH(srcTi)

    # CanvasPoints = np.float32([[0, 0], [1080, 0], [1080, 1440], [0, 1440]])
    CanvasPoints = np.float32([[0, 0],  [cols, 0],[cols, rows], [0, rows]])
    # print(SrcPoints)
    # print(CanvasPoints)

    SrcPointsA = np.array(SrcPoints, dtype=np.float32)
    CanvasPointsA = np.array(CanvasPoints, dtype=np.float32)
    PerspectiveMatrix = cv2.getPerspectiveTransform(np.array(SrcPointsA),
                                                    np.array(CanvasPointsA))
    PerspectiveImg = cv2.warpPerspective(Img, PerspectiveMatrix, (cols, rows))
    return PerspectiveImg



imapath = "/Users/developer/Downloads/52.jpg"
imaSave = '/Users/developer/Downloads/52_save.jpg'

Img = cv2.imread(imapath)
rows, cols, chan = Img.shape

rect = Main(imapath, imaSave)

# rect = [[0.2375, 0.140625], [0.8333333333333334, 0.1875], [0.7395833333333334, 0.8515625], [0.18958333333333333, 0.8203125]]
print("===========================================")
print(rect)

srcTi = [
        [int(rect[0][0] * cols), int(rect[0][1] * rows)],
        [int(rect[1][0] * cols), int(rect[1][1] * rows)],
        [int(rect[2][0] * cols), int(rect[2][1] * rows)],
        [int(rect[3][0] * cols), int(rect[3][1] * rows)],
    ]
# savePath = os.path.join(imageDir, 'crop' + filePath)
result = getCovertedImage(Img,srcTi)
cv2.imwrite(imaSave, result)


#
# if __name__ == '__main__':
#     imgType = ['jpeg', 'jpg', 'png']
#     for root, dirs, files in os.walk("/Users/developer/Downloads/", topdown=False):
        # for name in dirs:
        #     imageDir = os.path.join(root, name)
        #     for filePath in os.listdir(imageDir):
        #         if filePath.split('.')[-1] in imgType:
        #
        #             imgpath = os.path.join(imageDir, filePath)
        #             Img = cv2.imread(imgpath)
        #             rows, cols, chan = Img.shape
        #
        #             savePath = os.path.join(imageDir, 'cropPos' + filePath)
        #             rect = Main(imgpath, savePath)
        #
        #             print("===========================================")
        #             print(filePath)
        #             print(rect)
        #
        #             srcTi = [
        #                     [int(rect[0][0] * cols), int(rect[0][1] * rows)],
        #                     [int(rect[1][0] * cols), int(rect[1][1] * rows)],
        #                     [int(rect[2][0] * cols), int(rect[2][1] * rows)],
        #                     [int(rect[3][0] * cols), int(rect[3][1] * rows)],
        #                 ]
        #             savePath = os.path.join(imageDir, 'crop' + filePath)
        #             result = getCovertedImage(Img,srcTi)
        #             cv2.imwrite(savePath, result)

    # imageURL = '/Users/developer/Downloads/56.jpg'
    # Img = cv2.imread(imageURL)
    # rows, cols,chan = Img.shape
    #
    # filePath = imageURL.split("/")[-1]
    #
    # rect = ImageRecify(Img,filePath)
    # pos1 = rect[0]
    # pos2 = rect[1]
    # pos3 = rect[2]
    # pos4 = rect[3]
    #
    #
    # srcTi = [
    #         [pos1[0] * cols, pos1[1] * rows],
    #         [pos2[0] * cols, pos2[1] * rows],
    #         [pos3[0] * cols, pos3[1] * rows],
    #         [pos4[0] * cols, pos4[1] * rows],
    #     ]

    # srcTi = [
    #         [538, 154],
    #         [1028, 474],
    #         [552, 1274],
    #         [22, 926],
    #     ]

    # srcTi = [[0.14074073731899261, 0.918055534362793],
    #           [0.14074073731899261, 0.1180555522441864],
    #           [0.8425925970077515, 0.1180555522441864],
    #           [0.8425925970077515, 0.918055534362793]]

    # cv2.putText(Img, 'C1', (int(srcTi[0][0] * cols),int(srcTi[0][1] * rows)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    # cv2.putText(Img, 'C2', (int(srcTi[1][0] * cols),int(srcTi[1][1] * rows)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    # cv2.putText(Img, 'C3', (int(srcTi[2][0] * cols),int(srcTi[2][1] * rows)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    # cv2.putText(Img, 'C4', (int(srcTi[3][0] * cols),int(srcTi[3][1] * rows)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    # cv2.imwrite('./image/markedImag.jpg',Img)

    # result = getCovertedImage(Img,srcTi)
    # cv2.imwrite('./image/PerspectiveImg.png', result)


