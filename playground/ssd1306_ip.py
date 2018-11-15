#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################
# ssd1306_ip.py                                                             #
# (c) https://github.com/thomaspfeiffer-git 2017                            #
#############################################################################
"""display IP address on SSD1306. pretty useful right after startup."""

import socket
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


def my_ip ():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


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
_, textheight = draw.textsize("Text", font=font)

while True:
    draw.rectangle((0,0,width,height), outline=0, fill=255)
    y = ypos
    draw.text((xpos, y), "Zeit: {}".format(time.strftime("%X")), font=font, fill=0)
    y += textheight
    draw.text((xpos, y), "IP: {}".format(my_ip()), font=font, fill=0)

    disp.image(image)
    disp.display()
    time.sleep(10)


# eof #

