import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load an image using OpenCV
image_file = "data/page_01.jpg"
img = cv2.imread(image_file) # read the image file


# Display the image
def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)

    height, width  = im_data.shape[:2]
    
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()

# Display the image
#display(image_file)

# 1 Invert the image
inverted_img = cv2.bitwise_not(img)
cv2.imwrite("temp/inverted_image.jpg", inverted_img)

# Display the inverted image
#display("temp/inverted_image.jpg")


# 2 Convert to Binary
# Convert the image to grayscale
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  

gray_img = grayscale(img)
cv2.imwrite("temp/gray_image.jpg", gray_img)
#display("temp/gray_image.jpg")

# Convert the grayscale image to binary
# Pixels > 210 → Set to 230, 
#Pixels ≤ 210 → Set to 0
thresh, img_bin = cv2.threshold(gray_img, 210, 230, cv2.THRESH_BINARY)

cv2.imwrite("temp/binary_image.jpg", img_bin)
#display("tmp/binary_image.jpg")

# 3 Noise Removal
def remove_noise(image):
    # Apply dilation
    kernal = np.ones((1,1), np.uint8)
    # The number of iterations is the number of times the dilation is applied
    image = cv2.dilate(image, kernal, iterations=1)
    # Apply erosion
    kernal1 = np.ones((1,1), np.uint8)
    # The number of iterations is the number of times the erosion is applied
    image = cv2.erode(image, kernal1, iterations=1)
    image =cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernal1)
    image = cv2.medianBlur(image, 3)

    return (image)

img_noise_removed = remove_noise(img_bin)
cv2.imwrite("temp/noise_removed_image.jpg", img_noise_removed)
#display("temp/noise_removed_image.jpg")

# 4 Dilate and Erode the image
# erode the image to make the font thinner
def thin_font(image):
    image = cv2.bitwise_not(image)
    kernal = np.ones((2,2), np.uint8)
    image = cv2.erode(image, kernal, iterations=1)
    image = cv2.bitwise_not(image)
    return image

eroded_img = thin_font(img_noise_removed)
cv2.imwrite("temp/eroded_image.jpg", eroded_img)
#display("temp/eroded_image.jpg")

# dilate the image to make the font thicker
def thick_font(image):
    image = cv2.bitwise_not(image)
    kernal = np.ones((2,2), np.uint8)
    image = cv2.dilate(image, kernal, iterations=1)
    image = cv2.bitwise_not(image)
    return image

dilated_img = thick_font(img_noise_removed)
cv2.imwrite("temp/dilated_image.jpg", dilated_img)
#display("temp/dilated_image.jpg")

# 5 Rotate the image
new = cv2.imread("data/page_01_rotated.jpg")
#display("data/page_01_rotated.JPG")

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle
# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

# Deskew the image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)

fixed = deskew(new)
cv2.imwrite("temp/fixed.jpg", fixed)
#display("temp/fixed.jpg")

# 6 Remove the border
display("temp/noise_removed_image.jpg")

def remove_border(image):
    # Convert the image to grayscale
    contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Sort the contours by area
    cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x))
    # Get the largest contour needs to be -1
    cnt = cntsSorted[-1]
    # Get the bounding rectangle of the largest contour
    x, y, w, h = cv2.boundingRect(cnt)
    # Crop the image using the bounding
    crop = image[y:y+h, x:x+w]
    return (crop)

no_border = remove_border(img_noise_removed)   
cv2.imwrite("temp/no_border.jpg", no_border)
display("temp/no_border.jpg")

# 7 Adding border
color = [127, 127, 0]
top, bottom, left, right = [150]*4
img_with_border = cv2.copyMakeBorder(no_border, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
cv2.imwrite("temp/img_with_border.jpg", img_with_border)
display("temp/img_with_border.jpg")

