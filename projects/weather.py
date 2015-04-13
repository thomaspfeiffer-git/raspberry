#!/usr/bin/python
# coding=utf-8


###############################################################################
# weather.py                                                                  #
# weather station                                                             #
# several sensors (indoor, outdoor)                                           #
# rrd statistics                                                              #
# Version 0.2                                                                 #
# Thomas Pfeiffer                                                             #
# 2015                                                                        #
###############################################################################

import os
import sys
import traceback

import rrdtool
from Adafruit_BMP085 import BMP085
import RPi.GPIO as io
import dhtreader


## Sensors ##################
#+ Outdoor ##################
# DHT22/AM2302 (humidity, air pressure)
pin_sensor_outdoor     = 15
pin_sensor_outdoor_bcm = 22

#+ Indoor ###################
# DHT22/AM2302 (humidity, air pressure)
pin_sensor_indoor      = 32
pin_sensor_indoor_bcm  = 12


# BMP085 (air pressure)
bmp = 0


# Misc for rrdtool
DATAFILE       = "/schild/weather.rrd"
ERROR          = -999.99
DS_TEMPINDOOR  = "temp_indoor"   # Besser: Hash mit {DS:...; Name: "..."}
DS_TEMPOUTDOOR = "temp_outdoor"
DS_HUMIINDOOR  = "humi_indoor"
DS_HUMIOUTDOOR = "humi_outdoor"
DS_AIRPRESSURE = "air_pressure"
DS_TEMPCPU     = "temp_cpu"


# Other global stuff

bDebug  = False
PIDFile = ""


################################################################################
# Exit #########################################################################
def Exit():
   Log('Cleaning up ...')
   sys.exit()



################################################################################
# CheckPIDFile #################################################################
def CheckPIDFile():
   global PIDFile
   PIDFile = __file__ + ".pid"

   if (os.path.isfile(PIDFile)):
      Log("PID File exists. Don't start me twice!")
      Exit()

   f = open(PIDFile, 'w')
   f.write(str(os.getpid()))
   f.close()



################################################################################
# CleanupPIDFile ###############################################################
# Must no be called in Cleanup();                                              #
# this would delete the PID file of other processes                            #
def CleanupPIDFile():
   global PIDFile

   os.remove(PIDFile)



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

   i = 1                         # outdoor #
   while (i <= 5):
      try:
         Log("Outdoor, try #{}".format(i))
         temp_outdoor, humi_outdoor = dhtreader.read(22,pin_sensor_outdoor_bcm) 
      except TypeError:
         temp_outdoor = humi_outdoor = ERROR
         i += 1
         continue
      break


   i = 1                         # indoor #
   while (i <= 5):
      try:
         Log("Indoor, try #{}".format(i))
         temp_indoor, humi_indoor = dhtreader.read(22,pin_sensor_indoor_bcm) 
      except TypeError:
         temp_indoor = humi_indoor = ERROR
         i += 1
         continue
      break


#   temp_indoor = bmp.readTemperature()  # indoor #
   pressure    = bmp.readPressure()

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


################################################################################
try:
   bDebug = True if (len(sys.argv) > 1) and (sys.argv[1] in ['-v', '-V']) \
            else False

   CheckPIDFile()
   Init()
   Main()
   CleanupPIDFile()

except:
   print(traceback.print_exc())

finally:
   Exit()

