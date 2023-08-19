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

from flask import Flask
from flask_restful import Resource, Api
import os
import sys
import threading
import time

sys.path.append('../../libs')
sys.path.append('../../libs/sensors')

from i2c import I2C

from sensors.CPU import CPU
from sensors.BME680 import BME680, BME_680_BASEADDR
from sensors.TSL2561 import TSL2561

from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data

from Commons import Singleton
from Logging import Log
from Shutdown import Shutdown
import UDP


CREDENTIALS = os.path.expanduser("~/credentials/kitchen.cred")


##############################################################################
# Sensors ####################################################################
class Sensors (threading.Thread, metaclass=Singleton):
    def __init__ (self):
        threading.Thread.__init__(self)

        self.values = {'temp': "n/a",
                       'tempcpu': "n/a",
                       'humi': "n/a",
                       'airpressure': "n/a",
                       'lightness': "n/a",
                       'airquality': "n/a"}

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
        self.bme680  = BME680(i2c_addr=BME_680_BASEADDR, \
                              qv_temp=self.qv_temp, qv_humi=self.qv_humi, \
                              qv_pressure=self.qv_pressure, qv_airquality=self.qv_airquality)
        self.tsl2561 = TSL2561(qvalue=self.qv_light)

        self.udp = UDP.Sender(CREDENTIALS)

    def run (self):
        self._running = True
        while self._running:
            self.values['tempcpu']     = self.cpu.read_temperature()
            self.values['lightness']   = self.tsl2561.lux()
            self.bme680.get_sensor_data()
            self.values['temp']        = self.bme680.data.temperature
            self.values['humi']        = self.bme680.data.humidity
            self.values['airpressure'] = self.bme680.data.pressure
            self.values['airquality']  = self.bme680.data.air_quality_score \
                                         if self.bme680.data.air_quality_score != None else 0

            rrd_data = "N:{:.2f}".format(self.values['temp'])        + \
                        ":{:.2f}".format(self.values['tempcpu'])     + \
                        ":{:.2f}".format(self.values['humi'])        + \
                        ":{:.2f}".format(self.values['airpressure']) + \
                        ":{:.2f}".format(self.values['lightness'])   + \
                        ":{:.2f}".format(self.values['airquality'])  + \
                        ":{}".format(0)                              + \
                        ":{}".format(0)                              + \
                        ":{}".format(0)                              + \
                        ":{}".format(0)
            self.udp.send(rrd_data)

            for _ in range(50): # interruptible sleep
                if self._running:
                    time.sleep(1)
                    # brightness control needs higher frequency
                    self.values['lightness'] = self.tsl2561.lux()
                else:
                    break

    def stop (self):
        self._running = False


###############################################################################
# Flask stuff #################################################################
class API_Values (Resource):
    def get (self):
        return sensors.values


###############################################################################
# shutdown_application ########################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    # TODO: bme680.shutdown() while calculating baseline
    sensors.stop()
    sensors.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)
    app = Flask(__name__)

    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    api = Api(app)
    api.add_resource(API_Values, '/')

    sensors = Sensors()
    sensors.start()

    app.run(host="0.0.0.0", port=5001)

# eof #

