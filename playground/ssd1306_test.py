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
# from PIL import ImageDraw
# from PIL import ImageFont

sys.path.append('../libs')
from actuators.SSD1306 import SSD1306


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

