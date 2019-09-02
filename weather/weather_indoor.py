#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# weather_indoor.py                                                           #
# Monitors temperature, humidity, and air pressure in our living room.        #
# (c) https://github.com/thomaspfeiffer-git 2019                              #
###############################################################################
""" Collect weather and some other data indoor (mainly with BME680). """

# start with:
# nohup ./weather_indoor.py 2>weather_indoor.err >weather_indoor.err &

import rrdtool
import sys
import time

sys.path.append('../libs')

from sensors.BME680 import BME680, BME_680_BASEADDR
from sensors.CPU import CPU

from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data

from Logging import Log
from Shutdown import Shutdown


# Misc for rrdtool
DATAFILE      = "/schild/weather/weather_indoor.rrd"
DS_TEMP       = "temp" 
DS_HUMI       = "humi"
DS_PRESSURE   = "pressure"
DS_AIRQUALITY = "airquality"
DS_TEMPCPU    = "temp_cpu"


###############################################################################
# Main ########################################################################
def main():
    """main part"""

    qv_temp       = SensorValue("ID_01", "TempWohnzimmerIndoor", SensorValue_Data.Types.Temp, "°C")
    qv_humi       = SensorValue("ID_02", "HumiWohnzimmerIndoor", SensorValue_Data.Types.Humi, "% rF")
    qv_pressure   = SensorValue("ID_05", "Luftdruck", SensorValue_Data.Types.Pressure, "hPa") 
    qv_airquality = SensorValue("ID_14", "AirQualityWohnzimmer", SensorValue_Data.Types.AirQuality, "%")

    sq.register(qv_temp)
    sq.register(qv_humi)
    sq.register(qv_pressure)
    sq.register(qv_airquality)

    bme680 = BME680(i2c_addr=BME_680_BASEADDR, \
                    qv_temp=qv_temp, qv_humi=qv_humi, \
                    qv_pressure=qv_pressure, qv_airquality=qv_airquality)
    cpu = CPU.CPU()

    rrd_template = DS_TEMP       + ":" + \
                   DS_HUMI       + ":" + \
                   DS_PRESSURE   + ":" + \
                   DS_AIRQUALITY + ":" + \
                   DS_TEMPCPU

    while True:
        bme680.get_sensor_data()
        temp       = bme680.data.temperature
        humi       = bme680.data.humidity
        pressure   = bme680.data.pressure
        airquality = bme680.data.air_quality_score \
                     if bme680.data.air_quality_score != None else 0
        cpu_temp   = cpu.read_temperature()
     
        rrd_data = "N:" + \
                   ":".join("{:.2f}".format(d) for d in [temp,       \
                                                         humi,       \
                                                         pressure,   \
                                                         airquality, \
                                                         cpu_temp])
                                                          
        # Log(rrd_template)
        Log(rrd_data)
        rrdtool.update(DATAFILE, "--template", rrd_template, rrd_data) 
   
        sleep(50)


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

