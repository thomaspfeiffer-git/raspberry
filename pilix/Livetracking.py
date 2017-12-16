#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Livetracking.py                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################
"""
...

This lib can be used standalone as a receiver/server and imported into
another python program as a sender/client.
"""


### usage ###
# nohup ./Livetracking.py >livetracking.log 2>&1 &


import base64
import hashlib
import hmac
import socket
import sys
import threading
import time

sys.path.append("../libs/")
from Logging import Log

from config import CONFIG
from csv_fieldnames import *


###############################################################################
# Digest ######################################################################
class Digest (object):
    def __init__ (self, secret):
        self.__secret = secret.encode('utf-8')

    def __call__ (self, data):
        digest_maker = hmac.new(self.__secret, 
                                data.encode('utf-8'), 
                                hashlib.sha256) 
        return base64.encodestring(digest_maker.digest()).decode('utf-8').rstrip()


###############################################################################
# Sender ######################################################################
class Sender (threading.Thread):
    """sends some GPS data (lon, lat, alt, timestamp, voltage)
       to a server using UDP"""
    def __init__ (self):
        threading.Thread.__init__(self)
        self.digest = Digest(CONFIG.Livetracking.SECRET)
        self.data = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._running = True

    def setdata (self, data):
        self.data = data

    def run (self):
        while self._running:
            if self.data:
                payload = "{},{},{},{},{}".format(self.data[V_GPS_Time],
                                                  self.data[V_GPS_Lon],
                                                  self.data[V_GPS_Lat],
                                                  self.data[V_GPS_Alt],
                                                  self.data[V_Voltage])

                datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
                try:
                    sent = self.socket.sendto(datagram, 
                                              (CONFIG.Livetracking.IP_ADDRESS_SERVER,
                                               CONFIG.Livetracking.UDP_PORT))
                    Log("sent bytes: {}; data: {}".format(sent,datagram))
                except:
                    Log("Cannot send data: {0[0]} {0[1]}".format(sys.exc_info()))

            for _ in range(50):
                if self._running:
                    time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# Receiver ####################################################################
class Receiver (object):
    def __init__ (self):
        self.digest = Digest(CONFIG.Livetracking.SECRET)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((CONFIG.Livetracking.IP_ADDRESS_SERVER, 
                          CONFIG.Livetracking.UDP_PORT))
        self._running = True

    def run (self):
        while self._running:
            # TODO: exception handling
            datagram = self.socket.recv(CONFIG.Livetracking.MAX_PACKET_SIZE).decode('utf-8')
            (payload, digest_received) = datagram.rsplit(',', 1)
            if hmac.compare_digest(digest_received, self.digest(payload)):
                Log("Received data: {}".format(datagram))
                # TODO: use payload for whatever ...
            else:
                Log("Hashes do not match on data: {}".format(datagram))

    def stop (self):
        self._running = False


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    # s = Sender(None)
    # s.start()

    r = Receiver()
    r.run()

# eof #

