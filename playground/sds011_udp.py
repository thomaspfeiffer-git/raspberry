#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
##############################################################################
# ds011_udp.py                                                               #
# Testing air quality sensor SDS011                                          #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                  #
##############################################################################

import socket
import sys
import time

sys.path.append('../libs')

from Logging import Log
from Shutdown import Shutdown

from sensors.SDS011 import SDS011

sds011_1 = None
sds011_2 = None

CREDENTIALS = "/home/pi/credentials/weather.cred"


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    if sds011_1 is not None:
        sds011_1.close()
    if sds011_2 is not None:
        sds011_2.close()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# ToUDP #######################################################################
class ToUDP (object):
    def __init__ (self):
        import configparser as cfgparser
        from Commons import Digest

        self.cred = cfgparser.ConfigParser()
        self.cred.read(CREDENTIALS)

        self.SECRET = self.cred['UDP']['SECRET']
        self.IP_ADDRESS_SERVER = self.cred['UDP']['IP_ADDRESS_SERVER']
        self.UDP_PORT = int(self.cred['UDP']['UDP_PORT'])
        self.MAX_PACKET_SIZE = int(self.cred['UDP']['MAX_PACKET_SIZE'])

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.digest = Digest(self.SECRET)

    def send (self, id_, rrd_template, rrd_data):
        payload = "{},{}:{}".format("particulates_{}".format(id_),rrd_template,rrd_data)
        datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
        try:
            sent = self.socket.sendto(datagram, (self.IP_ADDRESS_SERVER, self.UDP_PORT))
            Log("Sent bytes: {}; data: {}".format(sent,datagram))
        except:
            Log("Cannot send data: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)
    udp = ToUDP()

    while True:
        sds011_1 = SDS011("/dev/ttyUSB0", use_query_mode=True)
        sds011_2 = SDS011("/dev/ttyUSB1", use_query_mode=True)

        sds011_1.sleep(sleep=False)
        time.sleep(1)
        sds011_2.sleep(sleep=False)
        time.sleep(25)

        for i in range(3):
            v1 = sds011_1.query();
            v2 = sds011_2.query();
            if v1 is not None and v2 is not None:
                # Log("PM2.5: {}; PM10: {}".format(values[0],values[1]))
                #print("{},{},{},{}".format(v1[0],v1[1],v2[0],v2[1]))
                Log(",{0[0]},{0[1]},{1[0]},{1[1]}".format(v1,v2))
                if i == 2:
                    udp.send(1,"1_pm25:1_pm10","N:{0[0]}:{0[1]}".format(v1))
                    udp.send(2,"2_pm25:2_pm10","N:{0[0]}:{0[1]}".format(v2))
            else:
                Log("v1 or v2 was None")
            time.sleep(3)    

        sds011_1.sleep()  
        time.sleep(1)
        sds011_2.sleep()  
        time.sleep(1)
        sds011_1 = None
        sds011_2 = None
        time.sleep(600)

# eof #

