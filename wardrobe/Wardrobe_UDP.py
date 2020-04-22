#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Wardrobe_UDP.py                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019, 2020             #
###############################################################################

"""
Purpose:
1) Send all data using UDP to my main server.
2) Receive data and store to rrd database.

This lib can be used either standalone as a receiver (2) or
imported to another python program as a sender (1).
"""

import configparser as cfgparser
import os
import socket
import sys

sys.path.append("../libs/")
from Commons import Digest
from Logging import Log

CREDENTIALS = os.path.expanduser("~/credentials/wardrobe.cred")
cred = cfgparser.ConfigParser()
cred.read(CREDENTIALS)

RRDFILE = os.path.expanduser("~/rrd/databases/wardrobe.rrd")


###############################################################################
# CONFIG ######################################################################
class CONFIG (object):
    SECRET = cred['UDP']['SECRET']
    IP_ADDRESS_SERVER = cred['UDP']['IP_ADDRESS_SERVER']
    UDP_PORT = int(cred['UDP']['UDP_PORT'])
    MAX_PACKET_SIZE = int(cred['UDP']['MAX_PACKET_SIZE'])


###############################################################################
# UDP_Sender ##################################################################
class UDP_Sender (object):
    def __init__ (self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.digest = Digest(CONFIG.SECRET)

    def send (self, data):
            payload = "{}".format(data)
            datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
            try:
                sent = self.socket.sendto(datagram,
                                          (CONFIG.IP_ADDRESS_SERVER, CONFIG.UDP_PORT))
                Log("Sent bytes: {}; data: {}".format(sent,datagram))
            except:
                Log("Cannot send data: {0[0]} {0[1]} (Data: {1})".format(sys.exc_info(), datagram))


###############################################################################
# UDP_Receiver ################################################################
class UDP_Receiver (object):
    DS_TEMP1     = "wr_temp1"
    DS_TEMPCPU   = "wr_tempcpu"
    DS_TEMP2     = "wr_temp2"
    DS_HUMI      = "wr_humi"
    DS_LIGHTNESS = "wr_lightness"
    DS_OPEN1     = "wr_open1"
    DS_OPEN2     = "wr_open2"
    DS_OPEN3     = "wr_open3"
    DS_OPEN4     = "wr_open4"
    rrd_template = DS_TEMP1     + ":" + \
                   DS_TEMPCPU   + ":" + \
                   DS_TEMP2     + ":" + \
                   DS_HUMI      + ":" + \
                   DS_LIGHTNESS + ":" + \
                   DS_OPEN1     + ":" + \
                   DS_OPEN2     + ":" + \
                   DS_OPEN3     + ":" + \
                   DS_OPEN4


    def __init__ (self):
        self.digest = Digest(CONFIG.SECRET)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((CONFIG.IP_ADDRESS_SERVER, CONFIG.UDP_PORT))

    def receive (self):
        import rrdtool
        while True:
            datagram = self.socket.recv(CONFIG.MAX_PACKET_SIZE).decode('utf-8')
            try:
                (rrd_data, digest) = datagram.rsplit(',', 1)
            except ValueError:
                Log("WARN: Payload corrupted: {}".format(payload))
            else:
                Log("RRD Data received: {}".format(rrd_data))
                try:                                      # TODO
                    rrdtool.update(RRDFILE, "--template", self.rrd_template, rrd_data)
                except rrdtool.OperationalError:
                    Log("Cannot update rrd database: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
# shutdown ####################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    from Shutdown import Shutdown
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    udp = UDP_Receiver()
    udp.receive()

# eof #

