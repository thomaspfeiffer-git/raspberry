#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Airparticulates.py                                                          #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                   #
###############################################################################

"""
Measures particulates (PM10, PM2.5) using an SDS011 sensor.
"""


### Usage ###
# nohup ./Airparticulates.py --id n >airparticulates.log 2>&1


import argparse
import socket
import sys
import threading
import time


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown

from sensors.SDS011 import SDS011

CREDENTIALS = "/home/pi/credentials/weather.cred"
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
        while self._running:
            sds011 = SDS011("/dev/ttyUSB0", use_query_mode=True)
            sds011.sleep(sleep=False)
            time.sleep(25)

            values = sds011.query();
            if values is not None:
                self.data = { self.PM25: values[0], self.PM10: values[1] }
                Log("Data read: PM25: {0[0]}, PM10: {0[1]}".format(values))
            else:
                Log("Reading SDS011 failed.")

            sds011.sleep()      
            time.sleep(1)
            sds011.close() # TODO: SDS011.__del__()
            time.sleep(5)
            sds011 = None

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

        self.rrd_pm25 = "{}_pm25".format(self.id)
        self.rrd_pm10 = "{}_pm10".format(self.id)
        self.rrd_template = "{}:{}".format(self.rrd_pm25,self.rrd_pm10)
        self.rrd_data = None

        self._running = True

    def store (self):
        raise NotImplementedError

    def run (self):
        while self._running:     
            for _ in range(int(UPDATE_INTERVAL*10/3)-100): # send UDP data frequently
                if not self._running:    # interruptible sleep 
                    break
                time.sleep(0.1)

            self.rrd_data = sensor.rrd # sending data after sleep() avoids 
            self.store()               # empty data in first loop cycle.

    def stop (self):
        self._running = False


###############################################################################
# ToUDP #######################################################################
class ToUDP (StoreData):
    def __init__ (self, id_):
        import configparser as cfgparser
        from Commons import Digest

        super().__init__(id_)

        self.cred = cfgparser.ConfigParser()
        self.cred.read(CREDENTIALS)

        self.SECRET = self.cred['UDP']['SECRET']
        self.IP_ADDRESS_SERVER = self.cred['UDP']['IP_ADDRESS_SERVER']
        self.UDP_PORT = int(self.cred['UDP']['UDP_PORT'])
        self.MAX_PACKET_SIZE = int(self.cred['UDP']['MAX_PACKET_SIZE'])

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.digest = Digest(self.SECRET)

    def store (self):
        payload = "{},{}:{}".format("particulates_{}".format(self.id),self.rrd_template,self.rrd_data)
        datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
        try:
            sent = self.socket.sendto(datagram, (self.IP_ADDRESS_SERVER, self.UDP_PORT))
            Log("Sent bytes: {}; data: {}".format(sent,datagram))
        except:
            Log("Cannot send data: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
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
    parser.add_argument('-i', '--id', required='True')
    args = parser.parse_args()

    sensor = Sensor()
    sensor.start()

    storedata = ToUDP(args.id)
    storedata.start()

    while True:
        time.sleep(0.5)

# eof #

