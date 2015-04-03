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
DATAFILE       = "weather.rrd"
ERROR          = -999.99
DS_TEMPINDOOR  = "temp_indoor"   # Besser: Hash mit {DS:...; Name: "..."}
DS_TEMPOUTDOOR = "temp_outdoor"
DS_HUMIINDOOR  = "humi_indoor"
DS_HUMIOUTDOOR = "humi_outdoor"
DS_AIRPRESSURE = "air_pressure"
DS_TEMPCPU     = "temp_cpu"



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
   global bmp

   humi_indoor = ERROR

   i = 1                         # outdoor #
   while (i <= 5):
      try:
         print("Try #{}".format(i))
         temp_outdoor, humi_outdoor = dhtreader.read(22,pin_sensor_bcm) 
      except TypeError:
         temp_outdoor = humi_outdoor = ERROR
         i += 1
         continue
      break

   temp_indoor = bmp.readTemperature()  # indoor #
   pressure    = bmp.readPressure()

   temp_cpu    = GetCPUTemperature()

# rrdtool update speed.rrd N:$speed


# DS_TEMPINDOOR  = "temp_indoor"   # Besser: Hash mit {DS:...; Name: "..."}
# DS_TEMPOUTDOOR = "temp_outdoor"
# DS_HUMIINDOOR  = "humi_indoor"
# DS_HUMIOUTDOOR = "humi_outdoor"
# DS_AIRPRESSURE = "air_pressure"
# DS_TEMPCPU     = "temp_cpu"



   rrd_template    = DS_TEMPINDOOR  + ":" + \
                     DS_TEMPOUTDOOR + ":" + \
                     DS_HUMIINDOOR  + ":" + \
                     DS_HUMIOUTDOOR + ":" + \
                     DS_AIRPRESSURE + ":" + \
                     DS_TEMPCPU
   rrd_writestring = "N:{:.2f}".format(temp_indoor)      + \
                      ":{:.2f}".format(temp_outdoor)     + \
                      ":{:.2f}".format(humi_indoor)      + \
                      ":{:.2f}".format(humi_outdoor)     + \
                      ":{:.2f}".format(pressure / 100.0) + \
                      ":{:.2f}".format(temp_cpu)



   print rrd_template
   print rrd_writestring

   print("CPU Temperatur: {:.2f} °C".format(temp_cpu))
   print("Temperatur DHT: {:.2f} °C".format(temp_outdoor))
   print("Luftfeuchtigkeit DHT: {:.2f} %".format(humi_outdoor))
   print("Temperatur BMP: {:.2f} °C".format(temp_indoor))
   print("Luftdruck BMP: {:.2f} hPa".format(pressure / 100.0))


################################################################################
try:
   Init()
   Main()

except:
   print(traceback.print_exc())

finally:
   Exit()

