import pytesseract
import cv2
import numpy as np


image = cv2.imread("data/smalltest.JPG")
base_image = image.copy()

# 1 Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 10))
dilate = cv2.dilate(thresh, kernal, iterations=1)
#cv2.imwrite("temp/sample_dilate.jpg", dilate)

# Find contours
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])

for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h > 20 and w > 250:
        roi = base_image[y:y+h, x:x+w]
        cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)


cv2.imwrite("temp/sample_boxes.jpg", image)
# before bounding box
#ocr_result_org = pytesseract.image_to_string(base_image)
#print(ocr_result_org)

# after bounding box
ocr_result = pytesseract.image_to_string(roi)
print(ocr_result)