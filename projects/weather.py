#!/usr/bin/python
# coding=utf-8


import os
import sys
import traceback

import rrdtool
from Adafruit_BMP085 import BMP085
import RPi.GPIO as io
import dhtreader


# Sensors ##################
pin_sensor     = 15
pin_sensor_bcm = 22

# Variables for BMP085
bmp = 0

# Misc for rrdtool
DATAFILE = "weather.rrd"
ERROR    = -999.99



################################################################################
# Exit #########################################################################
def Exit():
   Log('Cleaning up ...')
   sys.exit()


################################################################################
# Log ##########################################################################
def Log(l):
   print(l)


################################################################################
# Init #########################################################################
def Init():
   global bmp
   Log('Initializing ...')

   dhtreader.init()
   bmp = BMP085(0x77)

   Log('Initializing done.')


################################################################################
# GetCPUTemperature ############################################################
def GetCPUTemperature():
   res = os.popen('vcgencmd measure_temp').readline()
   return(float(res.replace("temp=","").replace("'C\n","")))


################################################################################
# Main #########################################################################
def Main():
   global state_led_big
   global bmp

   i = 1
   while (i <= 5):
      try:
         print("Try #{}".format(i))
         t, h = dhtreader.read(22,pin_sensor_bcm)
      except TypeError:
         t = h = -99.99
         i += 1
         continue
      break

   t_bmp = bmp.readTemperature()
   p_bmp = bmp.readPressure()
   CPUTemp = GetCPUTemperature()

# rrdtool update speed.rrd N:$speed




   print("CPU Temperatur: {:.2f} °C".format(CPUTemp))
   print("Temperatur DHT: {:.2f} °C".format(t))
   print("Luftfeuchtigkeit DHT: {:.2f} %".format(h))
   print("Temperatur BMP: {:.2f} °C".format(t_bmp))
   print("Luftdruck BMP: {:.2f} hPa".format(p_bmp / 100.0))


################################################################################
try:
   Init()
   Main()

except:
   print(traceback.print_exc())

finally:
   Exit()

