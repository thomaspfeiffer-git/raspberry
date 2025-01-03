#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Watchdog.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git 2024                              #
###############################################################################

"""
Sends pings to various Raspberrys to keep them awake (or reboot).
"""

import argparse
import datetime
import os
import socket
import sys
import threading
import time


sys.path.append("../libs/")
from Commons import MyIP
from Logging import Log
from Shutdown import Shutdown

HOSTS_TO_PING = ["nano01"]

PING_INTERVALL = 600  # intervall between pings (seconds)
TIMEOUT = 2 * 3600  # time (seconds) until reboot if no watchdog pings are received
# TIMEOUT = 10  # time until reboot if no watchdog pings are received



###############################################################################
# UDP #########################################################################
class UDP (object):
    def __init__ (self):
        self.UDP_PORT = 6666
        self.MAX_PACKET_SIZE = 128
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((MyIP(), self.UDP_PORT))

    def ping (self, destination):
        datagram = f"{destination}: {datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')}".encode('utf-8')
        try:
            sent = self.socket.sendto(datagram, (destination, self.UDP_PORT))
            Log(f"Sent bytes: {sent}; data: {datagram}")
        except:
            Log("Cannot send data: {0[0]} {0[1]} (Data: {1})".format(sys.exc_info(), datagram))

    def receive (self):
        datagram = self.socket.recv(self.MAX_PACKET_SIZE).decode('utf-8')
        # Log(f"Data received: {datagram}")
        return datagram


###############################################################################
# Receiver ####################################################################
class Receiver (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self.udp = UDP()
        self.timestamp = time.time()

    def run (self):
        self._running = True
        while self._running:
             data = self.udp.receive()
             Log(f"Data received: {data}")
             self.timestamp = time.time()

    def stop (self):
        self._running = False


###############################################################################
# Watchdog ####################################################################
def Watchdog ():
    while True:
        if receiver.timestamp + TIMEOUT < time.time():
            Log("No ping received. Rebooting in 5 seconds ...")
            time.sleep(5)
            os.system("reboot")

        time.sleep(0.1)


###############################################################################
# Sender ######################################################################
def Sender ():
    udp = UDP()
    while True:
        for host in HOSTS_TO_PING:
            udp.ping(host)

        for _ in range(PING_INTERVALL*10):
            time.sleep(0.1)


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    if args.receiver:
        receiver.stop()
        receiver.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--server", help="server: pings the clients as watchdog", action="store_true")
    group.add_argument("--receiver", help="receives watchdog pings", action="store_true")
    args = parser.parse_args()

    if args.server:
        Sender()

    if args.receiver:
        receiver = Receiver()
        receiver.start()
        Watchdog()

# eof #

