#!/usr/bin/python


import time

from PIL import Image
# from PIL import ImageDraw
# from PIL import ImageFont

import SSD1306


disp = SSD1306()

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()


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

