# -*- coding:utf-8 -*-
import sys
sys.path.append("../../../")

import cv2
import numpy as np

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

def getCovertedImage(Img,srcTi):
    SrcPoints = getOrderedPoints(srcTi)
    CanvasPoints = np.float32([[0, 0],  [cols, 0],[cols, rows], [0, rows]])
    print(SrcPoints)
    print(CanvasPoints)

    SrcPointsA = np.array(SrcPoints, dtype=np.float32)
    CanvasPointsA = np.array(CanvasPoints, dtype=np.float32)
    PerspectiveMatrix = cv2.getPerspectiveTransform(np.array(SrcPointsA),
                                                    np.array(CanvasPointsA))
    PerspectiveImg = cv2.warpPerspective(Img, PerspectiveMatrix, (cols, rows))
    return PerspectiveImg


if __name__ == '__main__':
    Img = cv2.imread('/Users/developer/Downloads/13.jpg')
    rows, cols,chan = Img.shape

    # srcTi = [
    #         [pos1[0], pos1[1]],
    #         [pos2[0], pos2[1]],
    #         [pos3[0], pos3[1]],
    #         [pos4[0], pos4[1]],
    #     ]

    # srcTi = [
    #         [538, 154],
    #         [1028, 474],
    #         [552, 1274],
    #         [22, 926],
    #     ]

    srcTi = [[0.14074073731899261, 0.918055534362793],
              [0.14074073731899261, 0.1180555522441864],
              [0.8425925970077515, 0.1180555522441864],
              [0.8425925970077515, 0.918055534362793]]

    cv2.putText(Img, 'C1', (int(srcTi[0][0] * cols),int(srcTi[0][1] * rows)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(Img, 'C2', (int(srcTi[1][0] * cols),int(srcTi[1][1] * rows)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(Img, 'C3', (int(srcTi[2][0] * cols),int(srcTi[2][1] * rows)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(Img, 'C4', (int(srcTi[3][0] * cols),int(srcTi[3][1] * rows)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.imwrite('./image/markedImag.jpg',Img)

    result = getCovertedImage(Img,srcTi)
    cv2.imwrite('./image/PerspectiveImg.png', result)


