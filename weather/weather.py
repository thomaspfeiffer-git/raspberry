#!/usr/bin/python
# -*- coding: utf-8 -*-
#############################################################################
# weather.py                                                                #
# Monitor temperature, humidity, and air pressure in our living room        #
# and outside.                                                              #
# (c) https://github.com/thomaspfeiffer-git 2015, 2016                      #
#############################################################################
"""Monitor temperature, humidity, and air pressure"""


import rrdtool
import signal
import sys
from threading import Lock
from time import sleep
import traceback


sys.path.append('../libs')
sys.path.append('../libs/sensors')
from BMP085 import BMP085
from CPU import CPU
from DHT22_AM2302 import DHT22_AM2302
from SensorQueue import SensorQueueClient_write
from SensorValue import SensorValueLock


## Sensors ##################
#+ Outdoor ##################
# DHT22/AM2302 (humidity, air pressure)
pin_sensor_outdoor     = 40
pin_sensor_outdoor_bcm = 21

#+ Indoor ###################
# DHT22/AM2302 (humidity, air pressure)
pin_sensor_indoor      = 38
pin_sensor_indoor_bcm  = 20


# Misc for rrdtool
DATAFILE       = "/schild/weather/weather.rrd"
ERROR          = -999.99
DS_TEMPINDOOR  = "temp_indoor" 
DS_TEMPOUTDOOR = "temp_outdoor"
DS_HUMIINDOOR  = "humi_indoor"
DS_HUMIOUTDOOR = "humi_outdoor"
DS_AIRPRESSURE = "air_pressure"
DS_TEMPCPU     = "temp_cpu"


# Other global stuff
bDebug = False


################################################################################
# Exit ########################################################################
def Exit():
    """cleanup stuff"""
    Log('Cleaning up ...')
    sq.stop()
    sq.join()
    sys.exit()

def _Exit(__s, __f):
    """cleanup stuff used for signal handler"""
    Exit()


################################################################################
# Log ##########################################################################
def Log(message):
    """prints debug messages"""
    if (bDebug):
        print(message)


################################################################################
# Main #########################################################################
def Main():
    """initialize lots of sensor values for the sensor value queue
       initialize the sensors
       poll the sensor in a loop and write data to rrd"""

    qvalue_temp_indoor  = SensorValueLock("ID_01", "TempWohnzimmerIndoor", "temp", u'°C', Lock())
    qvalue_humi_indoor  = SensorValueLock("ID_02", "HumiWohnzimmerIndoor", "humi", u'% rF', Lock())
    qvalue_temp_outdoor = SensorValueLock("ID_03", "TempWohnzimmerOutdoor", "temp", u'°C', Lock())
    qvalue_humi_outdoor = SensorValueLock("ID_04", "HumiWohnzimmerOutdoor", "humi", u'% rF', Lock())
    qvalue_pressure     = SensorValueLock("ID_05", "Luftdruck", "press", u'hPa', Lock())

    sq.register(qvalue_temp_indoor)
    sq.register(qvalue_humi_indoor)
    sq.register(qvalue_temp_outdoor)
    sq.register(qvalue_humi_outdoor)
    sq.register(qvalue_pressure)
    sq.start()

    tempcpu = CPU()
    th_indoor  = DHT22_AM2302(pin_sensor_indoor_bcm, qvalue_temp_indoor, qvalue_humi_indoor)
    th_outdoor = DHT22_AM2302(pin_sensor_outdoor_bcm, qvalue_temp_outdoor, qvalue_humi_outdoor)
    bmp085     = BMP085(qvalue_pressure)

    while(True):
        temp_indoor, humi_indoor   = th_indoor.read()
        temp_outdoor, humi_outdoor = th_outdoor.read()
        pressure                   = bmp085.read()
        temp_cpu                   = tempcpu.read()

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

        sleep(30)


################################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)
    bDebug = True if (len(sys.argv) > 1) and (sys.argv[1] in ['-v', '-V']) \
             else False

    try:
        sq = SensorQueueClient_write()
        Main()

    except KeyboardInterrupt:
        Exit()

    except SystemExit:                 # Done in signal handler (method _Exit()) #
        pass

    except:
        print(traceback.print_exc())

    finally:
        pass

# eof #

