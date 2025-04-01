import pytesseract
from PIL import Image
from matplotlib import pyplot as plt
import cv2
import numpy as np

Image_file = "data/index_02.jpg"
img = Image.open(Image_file)

# no preporcessing
# OCR the image
#ocr_result = pytesseract.image_to_string(img)
#print(ocr_result)


# Preprocessing the image before OCR using OpenCV and pytesseract 
# Idendify the structure of the image to make bounding boxes around the text
image = cv2.imread("data/index_02.jpg")
base_image = image.copy()
# 1 Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imwrite("temp/index_gray.jpg", gray)
# 2 blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# cv2.imwrite("temp/index_blur.jpg", gray)
# 3 threshold
thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# cv2.imwrite("temp/index_thresh.jpg", thresh)
# 4 dilate
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
# cv2.imwrite("temp/index_kernal.jpg", kernal)
dilate = cv2.dilate(thresh, kernal, iterations=1)
# cv2.imwrite("temp/index_dilate.jpg", dilate)
# 5 contours
# Find contours
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# Sort contours from left to right
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])
# Iterate over contours and draw bounding box

result = []

for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    # Filter out small contours
    if h > 200 and w > 20:
        roi = image[y:y+h, x:x+w]
        # cv2.imwrite("temp/index_roi.jpg", roi)
        cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)
        ocr_result = pytesseract.image_to_string(roi)
        ocr_result = ocr_result.split("\n")
        for item in ocr_result:
            result.append(item)

    # cv2.imwrite("temp/index_boxes.jpg", image)
   # print(result)
entities = []
for item in result:
    item = item.split(" ")[0]
    item = item.replace("\n", "")
    if len(item) > 2:
        if item[0] == "A" and "-" not in item:
            item = item.split(".")[0].replace(",", "").replace(";", "")
            entities.append(item)
            
print(entities)
print("----------------------------------")
entities = list(set(entities))  # remove duplicates
print(entities)
print("----------------------------------")
entities.sort()
print(entities)
print("----------------------------------")

