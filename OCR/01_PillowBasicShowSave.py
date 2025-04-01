from PIL import Image

im_file = "data/page_01.jpg"

im = Image.open(im_file)
#print(im.size) #size of the image
#im.show() shows the image in a window
#im.rotate(90).show() rotates the image by 90 degrees
im.rotate(180).show() # rotates the image by 180 degrees
im.save("temp/page_01_rotated.jpg") #saves the image to a file
