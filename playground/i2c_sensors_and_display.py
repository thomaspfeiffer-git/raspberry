#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# i2c_sensors.py                                                              #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Tests various i2c sensors"""


import sys
from time import sleep, strftime

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

sys.path.append('../libs')
sys.path.append('../libs/sensors')

import BME280    # air pressure, temperature, humidity
import BMP180    # air pressure, temperature
import DS1820    # temperature
import HTU21DF   # temperature, humidity
import MCP9808   # temperature
import TSL2561   # luminosity

import SSD1306   # display


bmp180  = BMP180.BMP180()
bme280  = BME280.BME280()

ds1820  = DS1820.DS1820("/sys/bus/w1/devices/28-000006b50d05/w1_slave")
htu21df = HTU21DF.HTU21DF()

MCP9808_1_ADDR = 0x18
MCP9808_2_ADDR = 0x19
mcp9808_1 = MCP9808.MCP9808(address=MCP9808_1_ADDR)
mcp9808_2 = MCP9808.MCP9808(address=MCP9808_2_ADDR)
tsl2561   = TSL2561.TSL2561()

display = SSD1306.SSD1306()


display.begin()
display.clear()
display.display()

width = display.width
height = display.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

xpos = 4
ypos = height / 2
velocity = 1
_, textheight = draw.textsize("Text", font=font)


while True:
     bmp180_pressure     = bmp180.read_pressure()/100.0
     bmp180_temperature  = bmp180.read_temperature()
     bme280_pressure     = bme280.read_pressure()/100.0
     bme280_temperature  = bme280.read_temperature()
     bme280_humidity     = bme280.read_humidity()
     # ds1820_temperature  = ds1820.read()
     ds1820_temperature  = -99.99
     htu21df_temperature = htu21df.read_temperature()
     htu21df_humidity    = htu21df.read_humidity()
     mcp9808_1_temp      = mcp9808_1.read_temperature()
     mcp9808_2_temp      = mcp9808_2.read_temperature()
     tsl2561_luminosity  = tsl2561.lux()
     
     values = ":".join("{:.2f}".format(d) for d in [bmp180_pressure,     \
                                                    bme280_pressure,     \
                                                    bme280_humidity,     \
                                                    htu21df_humidity,    \
                                                    bmp180_temperature,  \
                                                    bme280_temperature,  \
                                                    htu21df_temperature, \
                                                    mcp9808_1_temp,      \
                                                    mcp9808_2_temp,      \
                                                    ds1820_temperature,  \
                                                    tsl2561_luminosity])
     print(strftime("%X:"), values)

     draw.rectangle((0,0,width,height), outline=0, fill=255)
     y = ypos
     draw.text((xpos, y), "Druck: {:>8.2f} hPa".format(bmp180_pressure), font=font, fill=0)
     y += textheight
     draw.text((xpos, y), "Luftf.: {:>6.2f} % rF".format(bme280_humidity), font=font, fill=0)
     y += textheight
     draw.text((xpos, y), "Temp: {:>8.2f} C".format(bme280_temperature), font=font, fill=0)
     y += textheight
     draw.text((xpos, y), "Hell.: {:>8.2f} lux".format(tsl2561_luminosity), font=font, fill=0)
     y += textheight
     draw.text((xpos, y), "Druck: {:>8.2f} hPa".format(bmp180_pressure), font=font, fill=0)
     y += textheight
     draw.text((xpos, y), "Luftf.: {:>6.2f} % rF".format(bme280_humidity), font=font, fill=0)
     y += textheight
     draw.text((xpos, y), "Temp: {:>8.2f} C".format(bme280_temperature), font=font, fill=0)
     y += textheight
     draw.text((xpos, y), "Hell.: {:>8.2f} lux".format(tsl2561_luminosity), font=font, fill=0)

     l = tsl2561_luminosity if tsl2561_luminosity <= 255 else 255
     display.set_contrast(l)
     display.image(image)
     display.display()

#     print("BMP180     | Druck | {:>8.2f} | hPa     |".format(bmp180_pressure))
#     print("BME280     | Druck | {:>8.2f} | hPa     |".format(bme280_pressure))
#     print("BME280     | Humi  | {:>8.2f} | % rF    |".format(bme280_humidity))
#     print("HTU21DF    | Humi  | {:>8.2f} | % rF    |".format(htu21df_humidity))
#     print("BMP180     | Temp  | {:>8.2f} | C       |".format(bmp180_temperature))
#     print("BME280     | Temp  | {:>8.2f} | C       |".format(bme280_temperature))
#     print("HTU21DF    | Temp  | {:>8.2f} | C       |".format(htu21df_temperature))
#     print("MCP9808 #1 | Temp  | {:>8.2f} | C       |".format(mcp9808_1_temp))
#     print("MCP9808 #2 | Temp  | {:>8.2f} | C       |".format(mcp9808_2_temp))
#     print("DS1820     | Temp  | {:>8.2f} | C       |".format(ds1820_temperature))
#     print("TLS2561    | Hell  | {:>8.2f} | C       |".format(tsl2561_luminosity))
#     print("")

     sleep(1)

     ypos = ypos - velocity
     if ypos < -4 * textheight:
         ypos = height / 2

# eof #

