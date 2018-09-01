from flask import Flask
from flask import request
from base64 import b64decode
import numpy as np
import cv2
import json

from DetectEdge.Version1.ImageCorrect_V5 import ImageRecify

app = Flask(__name__)

@app.route('/detectEdge', methods=['GET', 'POST'])
def getEdge():
    argv = request.values
    imageData = b64decode(argv.get('image'))
    nparr = np.fromstring(imageData,np.uint8)
    image = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    positions = ImageRecify(image)
    result = {'position':positions.tolist()}
    return json.dumps(result)


@app.route('/OCR', methods=['GET', 'POST'])
def getOCR():
    result = {'position':'CCCCCCCCC'}
    return json.dumps(result)

if __name__ == '__main__':
    app.run()