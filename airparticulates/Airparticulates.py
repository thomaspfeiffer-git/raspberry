#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Airparticulates.py                                                          #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018, 2020             #
###############################################################################

"""
Measures particulates (PM10, PM2.5) using an SDS011 sensor.
"""


"""
###### Usage ######
### Sensor
nohup ./Airparticulates.py --sensor id 2>&1 > airparticulates.log &

### Receiver
nohup ./Airparticulates.py --receiver 2>&1 > airparticulates_udp.log &
"""

import argparse
import os
import rrdtool
import socket
import sys
import threading
import time


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown
import UDP

from sensors.SDS011 import SDS011

CREDENTIALS = os.path.expanduser("~/credentials/airparticulates.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/airparticulates.rrd")
UPDATE_INTERVAL = 10 * 60   # time delay between two measurements (seconds)


###############################################################################
# Sensor ######################################################################
class Sensor (threading.Thread):
    PM25 = 'pm25'
    PM10 = 'pm10'

    def __init__ (self):
        threading.Thread.__init__(self)
        self.data = { self.PM25: 0.0, self.PM10: 0.0 }
        self._running = True

    @property
    def rrd (self):
        return "N:{}:{}".format(self.data[self.PM25],self.data[self.PM10])

    def run (self):
        sds011 = SDS011("/dev/ttyUSB0", use_query_mode=True)
        while self._running:
            sds011.sleep(sleep=False)
            time.sleep(25)

            values = sds011.query();
            if values is not None:
                self.data = { self.PM25: values[0], self.PM10: values[1] }
                Log("Data read: PM25: {0[0]}, PM10: {0[1]}".format(values))
            else:
                Log("Reading SDS011 failed.")

            sds011.sleep()

            for _ in range(UPDATE_INTERVAL*10):  # interruptible sleep
                if not self._running:
                    break
                time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# StoreData ###################################################################
class StoreData (threading.Thread):
    def __init__ (self, id_):
        threading.Thread.__init__(self)
        self.id = id_

        self.udp = UDP.Sender(CREDENTIALS)

        self.rrd_pm25 = f"{self.id}_pm25"
        self.rrd_pm10 = f"{self.id}_pm10"
        self.rrd_template = f"{self.rrd_pm25}:{self.rrd_pm10}"

        self._running = True

    def run (self):
        while self._running:
            for _ in range(int(UPDATE_INTERVAL*10/3)-100): # send UDP data frequently
                if not self._running:
                    break
                time.sleep(0.1)

            if self._running:
                payload = "{},{}:{}".format("particulates_{}".format(self.id),self.rrd_template,sensor.rrd)
                self.udp.send(payload)

    def stop (self):
        self._running = False


###############################################################################
# Receiver ####################################################################
class Receiver (object):
    def __init__ (self):
        self.udp = UDP.Receiver(CREDENTIALS)

    def start (self):
        while True:
            data = self.udp.receive()
            Log(f"RRD Data received: {data}")
            try:
                rrdtool.update(RRDFILE, "--template", rrd_template, data)
            except rrdtool.OperationalError:
                Log("Cannot update rrd database: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    if args.sensor is not None:
        storedata.stop()
        storedata.join()
        sensor.stop()
        sensor.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sensor", help="read data from sensor and send to udp server", type=int)
    group.add_argument("--receiver", help="receive data via udp and store in rrd database", action="store_true")
    args = parser.parse_args()

    if args.receiver:
        r = Receiver()
        r.start()

    if args.sensor is not None:
        sensor = Sensor()
        sensor.start()

        storedata = StoreData(args.sensor)
        storedata.start()

        while True:
            time.sleep(0.5)

# eof #

