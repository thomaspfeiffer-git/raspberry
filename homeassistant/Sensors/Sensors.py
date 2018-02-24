#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
##############################################################################
# Sensors.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git 2018                             #
##############################################################################
"""
"""

### usage ###
# run programm: nohup ./Sensors.py &

import rrdtool
import sys
import time

sys.path.append('../../libs')
sys.path.append('../../libs/sensors')

from i2c import I2C

from sensors.CPU import CPU
from sensors.BME680 import BME680, BME_680_SECONDARYADDR
from sensors.TSL2561 import TSL2561

from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data

from Shutdown import Shutdown


# Misc for rrdtool
RRDFILE        = "/schild/weather/kitchen.rrd"
DS_TEMP        = "ki_temp"
DS_TEMPCPU     = "ki_tempcpu"
DS_HUMI        = "ki_humi"
DS_AIRPRESSURE = "ki_pressure"
DS_LIGHTNESS   = "ki_lightness"
DS_AIRQUALITY  = "ki_airquality"
DS_OPEN1       = "ki_open1"
DS_OPEN2       = "ki_open2"
DS_OPEN3       = "ki_open3"
DS_OPEN4       = "ki_open4"


###############################################################################
# shutdown_application ########################################################
def shutdown_application ():
    """called on shutdown; stops all threads"""
    print("in shutdown_application()")
    # TODO: bme680.shutdown() while calculating baseline
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    qv_temp       = SensorValue("ID_40", "TempKueche", SensorValue_Data.Types.Temp, "°C")
    qv_humi       = SensorValue("ID_41", "HumiKueche", SensorValue_Data.Types.Humi, "% rF")
    qv_pressure   = SensorValue("ID_42", "PressureKueche", SensorValue_Data.Types.Pressure, "hPa")
    qv_light      = SensorValue("ID_43", "LightKueche", SensorValue_Data.Types.Light, "lux")
    qv_airquality = SensorValue("ID_44", "AirQualityKueche", SensorValue_Data.Types.AirQuality, "%")

    sq = SensorQueueClient_write("../../../configs/weatherqueue.ini")
    sq.register(qv_temp)
    sq.register(qv_humi)
    sq.register(qv_pressure)
    sq.register(qv_light)
    sq.register(qv_airquality)

    cpu     = CPU()
    bme680  = BME680(i2c_addr=BME_680_SECONDARYADDR, \
                     qv_temp=qv_temp, qv_humi=qv_humi, \
                     qv_pressure=qv_pressure, qv_airquality=qv_airquality)
    tsl2561 = TSL2561(qvalue=qv_light)

    rrd_template = DS_TEMP        + ":" + \
                   DS_TEMPCPU     + ":" + \
                   DS_HUMI        + ":" + \
                   DS_AIRPRESSURE + ":" + \
                   DS_LIGHTNESS   + ":" + \
                   DS_AIRQUALITY  + ":" + \
                   DS_OPEN1       + ":" + \
                   DS_OPEN2       + ":" + \
                   DS_OPEN3       + ":" + \
                   DS_OPEN4

    while True:
        bme680.get_sensor_data()

        air_quality = bme680.data.air_quality_score if bme680.data.air_quality_score != None else 0
        rrd_data = "N:{:.2f}".format(bme680.data.temperature) + \
                    ":{:.2f}".format(cpu.read_temperature())  + \
                    ":{:.2f}".format(bme680.data.humidity)    + \
                    ":{:.2f}".format(bme680.data.pressure)    + \
                    ":{:.2f}".format(tsl2561.lux())           + \
                    ":{:.2f}".format(air_quality)             + \
                    ":{}".format(0)                           + \
                    ":{}".format(0)                           + \
                    ":{}".format(0)                           + \
                    ":{}".format(0)
        print(time.strftime("%Y%m%d %X:"), rrd_data)
        # rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)

        time.sleep(50)
    
# eof #

