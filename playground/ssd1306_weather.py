#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################
# ssd1306_weater.py                                                         #
# (c) https://github.com/thomaspfeiffer-git 2017                            #
#############################################################################
"""demo programm for display weather data on an SSD1306"""


### usage ###
# nohup ./ssd1306_weather.py &


# Packages you might install
# sudo pip3 install Pillow


from attrdict import AttrDict
from datetime import datetime
import json
import sys
import time
from urllib.request import urlopen

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

sys.path.append('../libs')
from actuators.SSD1306 import SSD1306


###############################################################################
# OWM #########################################################################
class OWM (object):
    def __init__ (self):
        self.data = None
        self.last_changed = None
        self._read()

    def _read (self):
        with urlopen("http://nano02:5000") as response:
            self.data = AttrDict(json.loads(response.read().decode("utf-8"))[1])
            self.last_changed = datetime.now().timestamp()
            # TODO: exception

    def __call__ (self):
        if self.last_changed + 60 < datetime.now().timestamp():
            self._read()
        return self.data


###############################################################################
# Display #####################################################################
class Display (SSD1306):
    def __init__ (self):
        super().__init__()
        self.begin()
        self.clear()
        self.display()

        self.xpos = 4
        self.ypos = self.y = 4

        self.img  = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.load_default()
        _, self.textheight = self.draw.textsize("Text", font=self.font)

    def reset (self):
        self.y = self.ypos
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=255)

    def text (self, text, offset=0):
        self.draw.text((self.xpos, self.y), text) 
        self.y += self.textheight + offset

    def show (self):
        self.image(self.img)
        self.display()


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    display = Display()
    owm = OWM()

    while True:
        display.reset()

        now  = datetime.now()
        data = owm()

        if now.second % 2:
            timestring = "{0}, {1.day}. {1.month}. {1.year}".format("Mo Di Mi Do Fr Sa So".split()[now.weekday()], now)
        else:
            timestring = "{0.hour:d}:{0.minute:02d}:{0.second:02d}".format(now)

        display.text(timestring, offset=3)
        display.text("{0.temp} C - {0.humidity} % rF".format(data).replace(".", ","))
        display.text("{}".format(data.desc))
        display.text("{}".format(data.time_text))
        display.show()

        time.sleep(0.1)

# eof #

