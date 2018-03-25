#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Airquality.py                                                               #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                   #
###############################################################################

"""
"""


import csv
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
from sensors.BME680 import BME680, BME_680_BASEADDR, BME_680_SECONDARYADDR


V_Timestamp = "Timestamp"
V_Temperature = "Temperature"
V_Humidity = "Humidity"
V_Pressure = "Pressure"
V_AirQuality = "Air Quality"


###############################################################################
# CSV #########################################################################
class CSV (object):
    fieldnames = [V_Timestamp, V_Temperature, V_Humidity, V_Pressure, V_AirQuality]
    filename   = "airquality.csv"

    def __init__ (self):
        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=',')
            writer.writeheader()

    def write (self, data):
        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=',')
            writer.writerow(data)


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

        self.draw.text((self.xpos, y), "{}".format(data[V_Timestamp]))
        y += self.textheight
        self.draw.text((self.xpos, y), "Temp: {:.1f} °C".format(data[V_Temperature]).replace('.', ','))
        y += self.textheight
        self.draw.text((self.xpos, y), "Humi: {:.1f} %".format(data[V_Humidity]).replace('.', ','))
        y += self.textheight
        self.draw.text((self.xpos, y), "Press: {:.1f} hPa".format(data[V_Pressure]).replace('.', ','))
        y += self.textheight
        if data[V_AirQuality] is not None:
            self.draw.text((self.xpos, y), "AirQ: {:.1f} %".format(data[V_AirQuality]).replace('.', ','))
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

    bme = BME680(i2c_addr=BME_680_SECONDARYADDR)
    csv_ = CSV()
    display = Display()

    while True:
        bme.get_sensor_data()

        data = { V_Timestamp: time.strftime("%Y%m%d %H:%M:%S"),
                 V_Temperature: bme.data.temperature,
                 V_Humidity: bme.data.humidity,
                 V_Pressure: bme.data.pressure,
                 V_AirQuality: bme.data.air_quality_score }

        display.showdata(data)
        csv_.write(data)
        # Log(data)
        time.sleep(5)

# eof #        

