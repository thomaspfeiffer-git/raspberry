#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################
# ssd1306_weater.py                                                         #
# (c) https://github.com/thomaspfeiffer-git 2017                            #
#############################################################################
"""demo programm for display weather data on an SSD1306"""


import json
import pprint
import sys
import time
from urllib.request import urlopen

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
_, textheight = draw.textsize("Text", font=font)

while True:
    draw.rectangle((0,0,width,height), outline=0, fill=255)
    y = ypos
    draw.text((xpos, y), "Zeit: {}".format(time.strftime("%X")), font=font, fill=0)
    y += textheight

    with urlopen("http://nano02:5000") as response:
        data = json.loads(response.read().decode("utf-8"))

    draw.text((xpos, y), "Temp: {} C".format(data[1]['temp']))
    y += textheight
    draw.text((xpos, y), "Humi: {} % rF".format(data[1]['humidity']))
    y += textheight
    draw.text((xpos, y), "{}".format(data[1]['desc']))
    y += textheight
    draw.text((xpos, y), "{}".format(data[1]['time_text']))
    y += textheight

    disp.image(image)
    disp.display()

    time.sleep(10)

# eof #

