#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################
# ssd1306_test.py                                                           #
# (c) https://github.com/thomaspfeiffer-git 2017                            #
#############################################################################
"""demo programm for display SSD1306"""

import sys
import time

# Packages you might install
# sudo pip3 install Pillow


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

sys.path.append('../libs')
from actuators.SSD1306 import SSD1306


disp = SSD1306()

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()


xpos = 4
ypos = 4
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

while True:
    draw.rectangle((0,0,width,height), outline=0, fill=255)
    y = ypos
    draw.text((xpos, y), "Zeit: {}".format(time.strftime("%X")), font=font, fill=0)
    disp.image(image)
    disp.display()


"""
while True:
    image = Image.open('katze.png').convert('1')
    disp.image(image)
    disp.display()
    time.sleep(1)
    image = Image.open('maus.png').convert('1')
    disp.image(image)
    disp.display()
    time.sleep(1)
"""

# eof #

