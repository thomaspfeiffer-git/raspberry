#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Airparticulates.py                                                          #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                   #
###############################################################################

"""
"""


### Usage ###
# nohup ./Airparticulates.py --local_rrd >airparticulates.log 2>&1
# nohup ./Airparticulates.py --remote_rrd >airparticulates.log 2>&1


import argparse
import sys
import threading
import time


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown

from sensors.SDS011 import SDS011

RRDFILE = "/schild/weather/airparticulates.rrd"
CREDENTIALS = "/home/pi/credentials/weather.cred"


###############################################################################
# Sensor ######################################################################
class Sensor (threading.Thread):
    PM25 = 'pm25'
    PM10 = 'pm10'

    def __init__ (self):
        threading.Thread.__init__(self)
        self._running = True
        self.data = { self.PM25: 0.0, self.PM10: 0.0 }

    @property
    def rrd (self):
        return "N:{}:{}".format(self.data[self.PM25],self.data[self.PM10])

    def run (self):
        while self._running:
            # faking sensor data
            from datetime import datetime
            h = datetime.now().hour
            m = datetime.now().minute
            self.data = { self.PM25: h*60 + m, self.PM10: 1440 - (h*60 + m) }

            for _ in range(600*5):  # interruptible sleep
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
            self.rrd_data = sensor.rrd
            Log(self.rrd_data)
            self.store()

            for _ in range(600*5-100):  # interruptible sleep
                if not self._running:
                    break
                time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# ToRRD #######################################################################
class ToRRD (StoreData):
    def __init__ (self):
        super().__init__(1)

    def store (self):    
        import rrdtool
        rrdtool.update(RRDFILE, "--template", self.rrd_template, self.rrd_data)


###############################################################################
# ToUDP #######################################################################
class ToUDP (StoreData):
    import configparser as cfgparser

    cred = cfgparser.ConfigParser()
    cred.read(CREDENTIALS)

    SECRET = cred['UDP']['SECRET']
    IP_ADDRESS_SERVER = cred['UDP']['IP_ADDRESS_SERVER']
    UDP_PORT = int(cred['UDP']['UDP_PORT'])
    MAX_PACKET_SIZE = int(cred['UDP']['MAX_PACKET_SIZE'])

    prefix = "pik_a_particulates"  # TODO: hostname

    def __init__ (self):
        import socket
        from Commons import Digest

        super().__init__(2)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.digest = Digest(self.SECRET)

    def store (self):
        payload = "{},{}:{}".format(self.prefix,self.rrd_template,self.rrd_data)
        datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
        try:
            sent = self.socket.sendto(datagram, 
                                      (self.IP_ADDRESS_SERVER, self.UDP_PORT))
            Log("Sent bytes: {}; data: {}".format(sent,datagram))
        except:
            Log("Cannot send data: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    sensor.stop()
    sensor.join()
    storedata.stop()
    storedata.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--local_rrd", help="runs with a local rrd database", action="store_true")
    group.add_argument("--remote_rrd", help="runs with a remote rrd database", action="store_true")
    args = parser.parse_args()

    sensor = Sensor()
    sensor.start()

    if args.local_rrd:
       storedata = ToRRD()
    if args.remote_rrd:
       storedata = ToUDP()

    storedata.start()

    while True:
        pass

# eof #

