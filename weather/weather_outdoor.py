#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# weather_outdoor.py                                                          #
# Monitors temperature, humidity, and air pressure outside                    #
# (c) https://github.com/thomaspfeiffer-git 2019                              #
###############################################################################
""" Collect weather and some other data outdoor. """

# start with:
# nohup ./weather_outdoor.py 2>weather_outdoor.err >weather_outdoor.err &

import rrdtool
import sys
import time

sys.path.append('../libs')

from sensors.BME280 import BME280
from sensors.CPU import CPU
from sensors.DS1820 import DS1820
from sensors.TSL2561 import TSL2561

from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data

from Logging import Log
from Shutdown import Shutdown


# Misc for rrdtool
DATAFILE       = "/schild/weather/weather_outdoor.rrd"
DS_TEMP        = "temp" 
DS_TEMP_GARDEN = "temp_gard" 
DS_HUMI        = "humi"
DS_PRESSURE    = "pressure"
DS_LIGHTNESS   = "lightness"
DS_TEMPCPU     = "temp_cpu"


###############################################################################
# Main ########################################################################
def main():
    """main part"""

    qv_temp        = SensorValue("ID_03", "TempOutdoor", SensorValue_Data.Types.Temp, "°C")
    qv_temp_garden = SensorValue("ID_12", "TempOutdoorGarden", SensorValue_Data.Types.Temp, "°C")
    qv_humi        = SensorValue("ID_04", "HumiOutdoor", SensorValue_Data.Types.Humi, "% rF")
    qv_lightness   = SensorValue("ID_15", "LightnessOutdoor", SensorValue_Data.Types.Light, "lux")

    sq.register(qv_temp)
    sq.register(qv_temp_garden)
    sq.register(qv_humi)
    sq.register(qv_lightness)

    bme280  = BME280(qvalue_pressure=qv_pressure, \
                     qvalue_temp=qv_temp,  \
                     qvalue_humi=qv_humi)
    ds1820  = DS1820("/sys/bus/w1/devices/28-000006d62eb1/w1_slave", qv_temp_garden)
    tsl2561 = TSL2561(qvalue=qv_lightness)
    cpu     = CPU()

    rrd_template = DS_TEMP        + ":" + \
                   DS_TEMP_GARDEN + ":" + \
                   DS_HUMI        + ":" + \
                   DS_PRESSURE    + ":" + \
                   DS_LIGHTNESS   + ":" + \
                   DS_TEMPCPU

    while True:
        temp        = bme280.read_temperature()
        temp_garden = ds1820.read_temperature()
        humi        = bme280.read_humidity()
        pressure    = bme280.read_pressure()/100.0 
        lightness   = tsl2561.lux()
        cpu_temp    = cpu.read_temperature()
     
        rrd_data = "N:" + \
                   ":".join("{:.2f}".format(d) for d in [temp,        \
                                                         temp_garden, \
                                                         humi,        \
                                                         pressure,    \
                                                         lightness,   \
                                                         cpu_temp])

        # Log(rrd_template)
        Log(rrd_data)
        rrdtool.update(DATAFILE, "--template", rrd_template, rrd_data) 
   
        time.sleep(50)


###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""
    sys.exit(0)


###############################################################################
###############################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    sq = SensorQueueClient_write("../../configs/weatherqueue.ini")
    main()

# eof #

