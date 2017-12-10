#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Livetracking.py                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################
"""
...

This library can be used standalone as a receiver/server and imported into
another python program as a sender/client.
"""


### usage ###


### needful things ###


### Packages you might need to install ###



import base64
import hashlib
import hmac
import socket
import sys
import threading
import time

sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown


# TODO: Config file! ##
secret  = "Nichts ist einfacher, als sich schwierig auszudrücken, und nichts ist schwieriger, als sich einfach auszudrücken."
IP_ADDRESS_SERVER = "213.143.107.230"
UDP_PORT = 20518
MAX_PACKET_SIZE = 128


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
    """sends some GPS data (lon, lat, height, timestamp 
       to a server using UDP"""
    def __init__ (self, gpsdata):
        threading.Thread.__init__(self)
        self.digest = Digest(secret)
        self.gpsdata = gpsdata
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._running = True

    def run (self):
        while self._running:
            lon = 47.1112208 # TODO: use self.gpsdata
            lat = 12.2232443
            z   = 471.2
            v   = 7.12
            t   = time.strftime("%Y%m%d%H%M%S")
            payload = "{},{},{},{},{}".format(t,lon,lat,z,v)

            datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
            # TODO: exception handling
            sent = self.socket.sendto(datagram, (IP_ADDRESS_SERVER, UDP_PORT))
            Log("sent bytes: {}; data: {}".format(sent,datagram))

            for _ in range(50):
                if self._running:
                    time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# Receiver ####################################################################
class Receiver (object):
    def __init__ (self):
        self.digest = Digest(secret)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((IP_ADDRESS_SERVER, UDP_PORT))
        self._running = True

    def run (self):
        while self._running:
            # TODO: exception handling
            datagram = self.socket.recv(MAX_PACKET_SIZE).decode('utf-8')
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
#    shutdown_application = Shutdown(shutdown_func=shutdown_application)


    s = Sender(None)
    s.start()

#    r = Receiver()
#    r.run()


# eof #

