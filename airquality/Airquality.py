#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Airquality.py                                                               #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                   #
###############################################################################

"""
"""


import sys
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

sys.path.append("../libs/")
from i2c import I2C
from Logging import Log
from Shutdown import Shutdown

from actuators.SSD1306 import SSD1306
from sensors.BME680 import BME680, BME_680_BASEADDR


###############################################################################
# Display #####################################################################
class Display (object):
    def __init__ (self):
        self.display = SSD1306()
        self.display.begin()
        self.display.clear()
        self.display.display()

        self.xpos = 4
        self.ypos = 4
        self.width = self.display.width
        self.height = self.display.height
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        (_, self.textheight) = self.draw.textsize("Text", font=self.font)

    def showdata (self, data):
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=255)
        y = self.ypos

        self.draw.text((self.xpos, y), "Temp: {} °C".format(data.temperature))
        y += self.textheight
        self.draw.text((self.xpos, y), "Humi: {} %".format(data.humidity))
        y += self.textheight
        self.draw.text((self.xpos, y), "Press: {} hPa".format(data.pressure))
        y += self.textheight
        self.draw.text((self.xpos, y), "AirQ: {} %".format(data.air_quality_score))
        y += self.textheight

        self.display.image(self.image)
        self.display.display()

    def close (self):    
        self.display.clear()
        self.display.display()


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    display.close()
    Log("Application stopped")
    sys.exit(0)


## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    bme = BME680(i2c_addr=BME_680_BASEADDR)
    display = Display()

    while True:
        bme.get_sensor_data()
        display.showdata(bme.data)
        Log("{:.2f} °C; {:.2f} hPa; {:.2f} % rF; gas resistance: {}; air quality: {}".format(bme.data.temperature, bme.data.pressure, bme.data.humidity, bme.data.gas_resistance, bme.data.air_quality_score))
        time.sleep(60)

# eof #        

