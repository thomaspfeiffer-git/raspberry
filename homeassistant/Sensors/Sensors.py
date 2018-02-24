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
import threading
import time

sys.path.append('../../libs')
sys.path.append('../../libs/sensors')

from i2c import I2C

from sensors.CPU import CPU
from sensors.BME680 import BME680, BME_680_SECONDARYADDR
from sensors.TSL2561 import TSL2561

from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data

from Commons import Singleton
from Logging import Log
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


class Sensors (threading.Thread, metaclass=Singleton):
    def __init__ (self):
        threading.Thread.__init__(self)

        self.qv_temp       = SensorValue("ID_40", "TempKueche", SensorValue_Data.Types.Temp, "°C")
        self.qv_humi       = SensorValue("ID_41", "HumiKueche", SensorValue_Data.Types.Humi, "% rF")
        self.qv_pressure   = SensorValue("ID_42", "PressureKueche", SensorValue_Data.Types.Pressure, "hPa")
        self.qv_light      = SensorValue("ID_43", "LightKueche", SensorValue_Data.Types.Light, "lux")
        self.qv_airquality = SensorValue("ID_44", "AirQualityKueche", SensorValue_Data.Types.AirQuality, "%")

        self.sq = SensorQueueClient_write("../../../configs/weatherqueue.ini")
        self.sq.register(self.qv_temp)
        self.sq.register(self.qv_humi)
        self.sq.register(self.qv_pressure)
        self.sq.register(self.qv_light)
        self.sq.register(self.qv_airquality)

        self.cpu     = CPU()
        self.bme680  = BME680(i2c_addr=BME_680_SECONDARYADDR, \
                              qv_temp=self.qv_temp, qv_humi=self.qv_humi, \
                              qv_pressure=self.qv_pressure, qv_airquality=self.qv_airquality)
        self.tsl2561 = TSL2561(qvalue=self.qv_light)

        self.rrd_template = DS_TEMP        + ":" + \
                            DS_TEMPCPU     + ":" + \
                            DS_HUMI        + ":" + \
                            DS_AIRPRESSURE + ":" + \
                            DS_LIGHTNESS   + ":" + \
                            DS_AIRQUALITY  + ":" + \
                            DS_OPEN1       + ":" + \
                            DS_OPEN2       + ":" + \
                            DS_OPEN3       + ":" + \
                            DS_OPEN4
        self._running = True

    def run (self):
        while self._running:

            self.bme680.get_sensor_data()

            air_quality = self.bme680.data.air_quality_score if self.bme680.data.air_quality_score != None else 0
            rrd_data = "N:{:.2f}".format(self.bme680.data.temperature) + \
                        ":{:.2f}".format(self.cpu.read_temperature())  + \
                        ":{:.2f}".format(self.bme680.data.humidity)    + \
                        ":{:.2f}".format(self.bme680.data.pressure)    + \
                        ":{:.2f}".format(self.tsl2561.lux())           + \
                        ":{:.2f}".format(air_quality)                  + \
                        ":{}".format(0)                                + \
                        ":{}".format(0)                                + \
                        ":{}".format(0)                                + \
                        ":{}".format(0)
            Log(rrd_data)
            # rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)

            for _ in range(50): # interruptible sleep
                if self._running:
                    time.sleep(0.1)
                else:
                    break

    def stop (self):
        self._running = False

   
###############################################################################
# Flask stuff #################################################################

 
###############################################################################
# shutdown_application ########################################################
def shutdown_application ():
    """called on shutdown; stops all threads"""
    print("in shutdown_application()")
    # TODO: bme680.shutdown() while calculating baseline
    sensors.stop()
    sensors.join()
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    sensors = Sensors()
    sensors.start()

    while True:
        pass

# eof #

