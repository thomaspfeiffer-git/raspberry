#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Airparticulates.py                                                          #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                   #
###############################################################################

"""
"""

import rrdtool
import sys
import threading
import time


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown

from sensors.SDS011 import SDS011

RRDFILE = "/schild/weather/airparticulates.rrd"


###############################################################################
# Sensor ######################################################################
class Sensor (threading.Thread):
    PM25 = 'pm25'
    PM10 = 'pm10'

    def __init__ (self):
        threading.Thread.__init__(self)
        self._running = True
        self.data = { self.PM25: 0.0, self.PM10: 0.0 }

    def run (self):
        while self._running:
            # faking sensor data
            from datetime import datetime
            self.data[self.PM25] = int(datetime.now().timestamp() % 2900)
            self.data[self.PM10] = int(2900 - (datetime.now().timestamp() % 2900))

            for _ in range(600):  # interruptible sleep
                if not self._running:
                    break
                time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# ToRRD #######################################################################
class ToRRD (threading.Thread):
    def __init__ (self, id_):
        threading.Thread.__init__(self)
        self.id = id_

        self.rrd_pm25 = "{}_pm25".format(self.id)
        self.rrd_pm10 = "{}_pm10".format(self.id)

        self._running = True

    def run (self):
        rrd_template = "{}:{}".format(self.rrd_pm25,self.rrd_pm10)
        # Log(rrd_template)
        while self._running:     
            # TODO: rrd_data = sensor.rrd
            rrd_data = "N:{}:{}".format(sensor.data[sensor.PM25],sensor.data[sensor.PM10])
            Log(rrd_data)
            rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)

            for _ in range(600):  # interruptible sleep
                if not self._running:
                    break
                time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    sensor.stop()
    sensor.join()
    to_rrd.stop()
    to_rrd.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    sensor = Sensor()
    sensor.start()
    to_rrd = ToRRD(id_=1)
    to_rrd.start()

    while True:
        pass

# eof #

