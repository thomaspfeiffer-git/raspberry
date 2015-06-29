#!/usr/bin/python
# coding=utf-8


###############################################################################
# weather.py                                                                  #
# weather station                                                             #
# several sensors (indoor, outdoor)                                           #
# rrd statistics                                                              #
# Version 1.0
# Thomas Pfeiffer                                                             #
# 2015                                                                        #
###############################################################################

import os
import numpy as np
import signal
import sys
from time import sleep
import traceback

import rrdtool
from Adafruit_BMP085 import BMP085
import RPi.GPIO as io

from DHT22_AM2302 import DHT22_AM2302


## Sensors ##################
#+ Outdoor ##################
# DHT22/AM2302 (humidity, air pressure)
pin_sensor_outdoor     = 40
pin_sensor_outdoor_bcm = 21

#+ Indoor ###################
# DHT22/AM2302 (humidity, air pressure)
pin_sensor_indoor      = 38
pin_sensor_indoor_bcm  = 20


# BMP085 (air pressure)
bmp = 0


# Misc for rrdtool
DATAFILE       = "/schild/weather/weather.rrd"
ERROR          = -999.99
DS_TEMPINDOOR  = "temp_indoor"   # Besser: Hash mit {DS:...; Name: "..."}
DS_TEMPOUTDOOR = "temp_outdoor"
DS_HUMIINDOOR  = "humi_indoor"
DS_HUMIOUTDOOR = "humi_outdoor"
DS_AIRPRESSURE = "air_pressure"
DS_TEMPCPU     = "temp_cpu"


# Other global stuff
bDebug  = False


################################################################################
# Exit ########################################################################
def Exit():
   Log('Cleaning up ...')
   sys.exit()

def _Exit(s,f):
   Exit()


################################################################################
# Log ##########################################################################
def Log(l):
   if (bDebug):
      print(l)


################################################################################
# Init #########################################################################
def Init():
   global bmp
   Log('Initializing ...')
   bmp = BMP085(0x77,2) 
   Log('Initializing done.')


################################################################################
# GetCPUTemperature ############################################################
def GetCPUTemperature():
   res = os.popen('vcgencmd measure_temp').readline()
   return(float(res.replace("temp=","").replace("'C\n","")))


################################################################################
# getPressure ##################################################################
def getPressure(sensor):
   p = []

   for i in range(0,10):
      p.append(sensor.readPressure())
   p.sort()

   p_avg = np.mean(p[int(len(p)/3):int(len(p)/3)*2])
   return p_avg


################################################################################
# Main #########################################################################
def Main():
   global bmp

   th_indoor  = DHT22_AM2302(pin_sensor_indoor_bcm)
   th_outdoor = DHT22_AM2302(pin_sensor_outdoor_bcm)

   while(True):
      temp_indoor, humi_indoor   = th_indoor.read()
      temp_outdoor, humi_outdoor = th_outdoor.read()
      pressure    = getPressure(bmp)
      temp_cpu    = GetCPUTemperature()

      rrd_template    = DS_TEMPINDOOR  + ":" + \
                        DS_TEMPOUTDOOR + ":" + \
                        DS_HUMIINDOOR  + ":" + \
                        DS_HUMIOUTDOOR + ":" + \
                        DS_AIRPRESSURE + ":" + \
                        DS_TEMPCPU

      rrd_data = "N:{:.2f}".format(temp_indoor)      + \
                  ":{:.2f}".format(temp_outdoor)     + \
                  ":{:.2f}".format(humi_indoor)      + \
                  ":{:.2f}".format(humi_outdoor)     + \
                  ":{:.2f}".format(pressure / 100.0) + \
                  ":{:.2f}".format(temp_cpu)

      rrdtool.update(DATAFILE, "--template", rrd_template, rrd_data) 
   
      Log(rrd_template)
      Log(rrd_data)

      Log("CPU Temperatur: {:.2f} °C".format(temp_cpu))
      Log("Temperatur DHT (outdoor): {:.2f} °C".format(temp_outdoor))
      Log("Luftfeuchtigkeit DHT (outdoor): {:.2f} %".format(humi_outdoor))
      Log("Temperatur DHT (indoor): {:.2f} °C".format(temp_indoor))
      Log("Luftfeuchtigkeit DHT (indoor): {:.2f} %".format(humi_indoor))
      Log("Temperatur BMP: {:.2f} °C".format(temp_indoor))
      Log("Luftdruck BMP: {:.2f} hPa".format(pressure / 100.0))

      sleep(50)


################################################################################
signal.signal(signal.SIGTERM, _Exit)
bDebug = True if (len(sys.argv) > 1) and (sys.argv[1] in ['-v', '-V']) \
         else False

try:
   Init()
   Main()

except KeyboardInterrupt:
   Exit()

except SystemExit:                  # Done in signal handler (method _Exit()) #
   pass

except:
   print(traceback.print_exc())

finally:
   pass


