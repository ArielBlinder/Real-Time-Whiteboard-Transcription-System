import pytesseract
from PIL import Image
from matplotlib import pyplot as plt

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

img_file = "data/page_01.jpg"
#display(img_file)
no_noise ="temp/noise_removed_image.jpg"
#display(no_noise)

img = Image.open(no_noise)

# OCR the image
ocr_result = pytesseract.image_to_string(img)
print(ocr_result)
