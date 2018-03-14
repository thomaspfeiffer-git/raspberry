#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# udp.py                                                                      #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                   #
###############################################################################
"""
Basic data transfer using UDP.
"""


import argparse
import base64
import configparser as cfgparser
import hashlib
import hmac
import socket
import sys
import time

sys.path.append("../../libs/")
from Logging import Log
from Shutdown import Shutdown


CREDENTIALS = "udp.cred"
cred = cfgparser.ConfigParser()
cred.read(CREDENTIALS)


###############################################################################
# CONFIG ######################################################################
class CONFIG (object):
    SECRET = cred['UDP']['SECRET']
    IP_ADDRESS_SERVER = cred['UDP']['IP_ADDRESS_SERVER']
    IP_ADDRESS_LOCAL = cred['UDP']['IP_ADDRESS_LOCAL']
    UDP_PORT = int(cred['UDP']['UDP_PORT'])
    MAX_PACKET_SIZE = int(cred['UDP']['MAX_PACKET_SIZE'])


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
class Sender (object):
    def __init__ (self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.digest = Digest(CONFIG.SECRET)
        self._running = True

    def run (self):
        while self._running:
            payload = "Daten via UDP: {}".format(time.strftime("%Y%m%d %X"))
            datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
            try:
                sent = self.socket.sendto(datagram, 
                                          (CONFIG.IP_ADDRESS_SERVER, 
                                          CONFIG.UDP_PORT))
                Log("Sent bytes: {}; data: {}".format(sent,datagram))
            except:
                Log("Cannot send data: {0[0]} {0[1]}".format(sys.exc_info()))

            time.sleep(5)

    def stop (self):
        self._running = False


###############################################################################
# Receiver ####################################################################
class Receiver (object):
    def __init__ (self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((CONFIG.IP_ADDRESS_LOCAL, CONFIG.UDP_PORT))
        self._running = True

    def run (self):
        while self._running:
            datagram = self.socket.recv(CONFIG.MAX_PACKET_SIZE).decode('utf-8')
            Log("Received: {}".format(datagram))

    def stop (self):
        self._running = False


###############################################################################
# shutdown ####################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    udp.stop()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--send", help="send data", action="store_true")
    group.add_argument("--receive", help="receive data", action="store_true")
    args = parser.parse_args()

    if args.send:
        udp = Sender()
    if args.receive:
        udp = Receiver()

    udp.run()    

# eof #

