#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################
# ssd1306_weater.py                                                         #
# (c) https://github.com/thomaspfeiffer-git 2017                            #
#############################################################################
"""demo programm for display weather data on an SSD1306"""


from datetime import datetime
import json
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



def read_owm ():
    with urlopen("http://nano02:5000") as response:
        data = json.loads(response.read().decode("utf-8"))
        # TODO: exception
    return data


def owm ():
    last_changed = datetime.now().timestamp()
    data = read_owm()

    def update ():
        nonlocal last_changed
        nonlocal data

        now = datetime.now().timestamp()
        if last_changed + 60 < now:
            last_changed = now
            data = read_owm()
        return data

    return update

get_data_from_owm = owm()


while True:
    draw.rectangle((0,0,width,height), outline=0, fill=255)
    y = ypos
    now = datetime.now()
    if now.second % 2:
        timestring = "{0}, {1.day}. {1.month}. {1.year}".format(["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"][now.weekday()], now)
    else:
        timestring = "{0.hour:d}:{0.minute:02d}:{0.second:02d}".format(now)

    draw.text((xpos, y), timestring, font=font, fill=0)
    y += textheight + 3

    data = get_data_from_owm()

    temp_humi = "{0} C - {1} % rF".format(data[1]['temp'], data[1]['humidity']).replace(".", ",")
    draw.text((xpos, y), temp_humi)
    y += textheight
    draw.text((xpos, y), "{}".format(data[1]['desc']))
    y += textheight
    draw.text((xpos, y), "{}".format(data[1]['time_text']))
    y += textheight

    disp.image(image)
    disp.display()

    time.sleep(0.1)

# eof #

