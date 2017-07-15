# -*- coding: utf-8 -*-
############################################################################
# Forecast.py                                                              #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""
   TODO
"""


from attrdict import AttrDict
from datetime import datetime
import json
import sys
import threading
import time
from urllib.error import HTTPError, URLError 
from urllib.request import urlopen

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

sys.path.append('../libs')
from actuators.SSD1306 import SSD1306
from Logging import Log


###############################################################################
# OWM #########################################################################
class OWM (object):
    def __init__ (self):
        self.data = None
        self.last_changed = None
        self._read()

    def _read (self):
        try:
            with urlopen("http://nano02:5000") as response:  # TODO: use config file
                self.data = AttrDict(json.loads(response.read().decode("utf-8"))[1])
        except (HTTPError, URLError):
            Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
        else:
            self.last_changed = datetime.now().timestamp()

    def __call__ (self):
        if self.last_changed + 60 < datetime.now().timestamp():
            self._read()
        return self.data


###############################################################################
# Display #####################################################################
class Display (SSD1306):
    def __init__ (self, central_i2c_lock):
        super().__init__()
        self.central_i2c_lock = central_i2c_lock
        self.begin()
        self.clear()
        with self.central_i2c_lock: 
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
        with self.central_i2c_lock:
            self.display()


###############################################################################
# Forecast ####################################################################
class Forecast (threading.Thread):
    def __init__ (self, central_i2c_lock):
        threading.Thread.__init__(self)
        self.display = Display(central_i2c_lock)
        self.owm = OWM()
        self.__running = True


    def run (self):
        while self.__running:
            self.display.reset()

            now  = datetime.now()
            data = self.owm()

            timestring = "{0}, {1.day}. {1.month}.; {1.hour:d}:{1.minute:02d}".format("Mo Di Mi Do Fr Sa So".split()[now.weekday()], now)
            self.display.text(timestring, offset=3)
            self.display.text("{0.temp} °C - {0.humidity} % rF".format(data).replace(".", ","))
            self.display.text("{}".format(data.desc))
            self.display.text("{}".format(data.time_text))
            self.display.show()

            time.sleep(1)

    def stop (self):
        self.__running = False

# eof #

