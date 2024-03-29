#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# UDP.py                                                                      #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2020, 2021             #
###############################################################################

"""
TODO
"""

import configparser
import os
import socket
import sys

sys.path.append("../libs/")
from Commons import Digest
from Logging import Log


###############################################################################
###############################################################################
class UDP (object):
    def __init__ (self, credentials_file):

        if not os.path.isfile(credentials_file):
            raise FileNotFoundError(f"File '{credentials_file}' does not exist!")

        credentials = configparser.ConfigParser()
        credentials.read(credentials_file)

        self.SECRET = credentials['UDP']['SECRET']
        self.IP_ADDRESS_SERVER = credentials['UDP']['IP_ADDRESS_SERVER']
        self.UDP_PORT = int(credentials['UDP']['UDP_PORT'])
        self.MAX_PACKET_SIZE = int(credentials['UDP']['MAX_PACKET_SIZE'])


###############################################################################
###############################################################################
class Sender (UDP):
    def __init__ (self, credentials_file):
        super().__init__(credentials_file)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.digest = Digest(self.SECRET)

    def send (self, data, log=True):
        payload = f"{data}"
        datagram = f"{payload},{self.digest(payload)}".encode('utf-8')
        try:
            sent = self.socket.sendto(datagram, (self.IP_ADDRESS_SERVER, self.UDP_PORT))
            if log:
                Log(f"Sent bytes: {sent}; data: {datagram}")
        except:
            Log("Cannot send data: {0[0]} {0[1]} (Data: {1})".format(sys.exc_info(), datagram))


###############################################################################
###############################################################################
class DatagramError (ValueError):
    def __init__ (self, datagram):
        self.datagram = datagram


###############################################################################
###############################################################################
class Receiver (UDP):
    def __init__ (self, credentials_file):
        super().__init__(credentials_file)
        self.digest = Digest(self.SECRET)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.IP_ADDRESS_SERVER, self.UDP_PORT))

    def receive (self, log=True):
        datagram = self.socket.recv(self.MAX_PACKET_SIZE).decode('utf-8')
        try:
            (data, digest) = datagram.rsplit(',', 1)
            if log:
                Log(f"Data received: {data}")
            # TODO verify digest
        except ValueError:
            Log(f"WARN: Payload corrupted: {datagram}")
            raise DatagramError(datagram)
        else:
            return data

# eof #
