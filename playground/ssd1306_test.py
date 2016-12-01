#!/usr/bin/python


import time

from PIL import Image
# from PIL import ImageDraw
# from PIL import ImageFont

from ssd1306 import SSD1306


disp = SSD1306()

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height


while True:
    image = Image.open('katze.png').convert('1')
    disp.image(image)
    disp.display()
    time.sleep(1)
    image = Image.open('maus.png').convert('1')
    disp.image(image)
    disp.display()
    time.sleep(1)



# eof #

