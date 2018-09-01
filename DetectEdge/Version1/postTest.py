import requests
from base64 import b64encode

# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion3/testImage3.jpg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion3/testImage4.jpg"

imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion1/testImage1.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion1/testImage2.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion1/testImage3.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion1/testImage4.jpeg"
# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion1/testImage5.jpeg"

# imagePath = "/Users/developer/Documents/OCR/Correct/imageVersion4/imageTest3.jpg"

with open(imagePath,'rb') as jpg_file:
    byte_content = jpg_file.read()
base64_string = b64encode(byte_content)
postArgv = {
    'image':base64_string
}
r = requests.post('http://localhost:5000/detectEdge',data = postArgv)
print(r.text)