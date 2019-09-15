# -*- coding: utf-8 -*-
###############################################################################
# UDP.py                                                                      #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                   #
###############################################################################

"""
TODO
"""

import configparser as cfgparser
import socket
import sys
import threading
import time


sys.path.append("../libs/")
from Commons import Digest
from Logging import Log


CREDENTIALS = "/home/pi/credentials/pool.cred"
cred = cfgparser.ConfigParser()
cred.read(CREDENTIALS)


###############################################################################
# CONFIG ######################################################################
class CONFIG (object):
    SECRET = cred['UDP']['SECRET']
    IP_ADDRESS_SERVER = cred['UDP']['IP_ADDRESS_SERVER']
    UDP_PORT = int(cred['UDP']['UDP_PORT'])
    MAX_PACKET_SIZE = int(cred['UDP']['MAX_PACKET_SIZE'])


###############################################################################
# UDP_Sender ##################################################################
class UDP_Sender (threading.Thread):
    def __init__ (self, data):
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.digest = Digest(CONFIG.SECRET)
        self.data = data
        self._running = True

    def send (self):
        if self.data.valid:
            payload = "{}".format(self.data.rrd) # TODO
            datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
            try:
                sent = self.socket.sendto(datagram, 
                                          (CONFIG.IP_ADDRESS_SERVER, 
                                          CONFIG.UDP_PORT))
                Log("Sent bytes: {}; data: {}".format(sent,datagram))
            except:
                Log("Cannot send data: {0[0]} {0[1]}".format(sys.exc_info()))

    def run (self):
        while self._running:
            self.send()
            for _ in range(600):      # interruptible sleep 
                if not self._running:
                    break
                time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# UDP_Receiver ################################################################
class UDP_Receiver (object):
    def __init__ (self):
        self.digest = Digest(CONFIG.Livetracking.SECRET)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((CONFIG.Livetracking.IP_ADDRESS_SERVER, 
                          CONFIG.Livetracking.UDP_PORT))

    def receive (self):
        while True:
            datagram = self.socket.recv(CONFIG.Livetracking.MAX_PACKET_SIZE).decode('utf-8')
            Log(datagram)

# eof #

