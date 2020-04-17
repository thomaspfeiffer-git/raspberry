#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Airparticulates_UDP.py                                                      #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018, 2020             #
###############################################################################
"""
Gets data from air quality sensor SDS011 via UDP and stores them in rrd.
"""

### usage ####
# nohup ./Airparticulates_UDP.py 2>&1 > ./airparticulates_udp.py &


import configparser as cfgparser
import os
import rrdtool
import socket
import sys
import threading
import time

sys.path.append('../libs')

from Commons import Digest
from Logging import Log
from Shutdown import Shutdown

CREDENTIALS = os.path.expanduser("~/credentials/airparticulates.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/airparticulates.rrd")

particulates_1 = "particulates_1"
particulates_2 = "particulates_2"
Particulates = [particulates_1, particulates_2]

data = { p: None for p in Particulates }


###############################################################################
# UDP_Receiver ################################################################
class UDP_Receiver (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

        cred = cfgparser.ConfigParser()
        cred.read(CREDENTIALS)

        self.SECRET = cred['UDP']['SECRET']
        self.UDP_PORT = int(cred['UDP']['UDP_PORT'])
        self.MAX_PACKET_SIZE = int(cred['UDP']['MAX_PACKET_SIZE'])

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.my_ip(), self.UDP_PORT))
        self.socket.setblocking(False)
        self.digest = Digest(self.SECRET)

    @staticmethod
    def my_ip ():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
            return IP

    def process_data (self, datagram):
        (payload, digest_received) = datagram.rsplit(',', 1)
        # TODO: verify digest
        (source, values) = payload.split(',')
        data[source] = values
        # data['particulates_2'] = "2_pm25:2_pm10:N:11.1:5.5"
        # Log("Data: {}".format(data))

    def run (self):
        self._running = True
        while self._running:
            try:
                datagram = self.socket.recv(self.MAX_PACKET_SIZE).decode('utf-8')
                Log("Received: {}".format(datagram))
                self.process_data(datagram)
            except BlockingIOError:
                for _ in range(50):  # interruptible sleep
                    if not self._running:
                        break
                    time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# ToRRD #######################################################################
class ToRRD (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

    @staticmethod
    def update_rrd (db, template, data):
        template = template.rstrip(":")
        data     = data.rstrip(":")
        retries  = 0
        # Log(template)
        # Log(data)
        while retries < 3:
            try:
                rrdtool.update(db, "--template", template, data)
                break
            except rrdtool.OperationalError:
                Log("Retry: #{0}. Cannot update rrd database: {1[0]} {1[1]}".format(retries,sys.exc_info()))
                time.sleep(1)
                retries += 1

    def rrd_particulates (self):
        data_complete = True
        rrd_template = ""
        rrd_data = "N:"
        for p in Particulates:
            if not data[p]:
                data_complete = False
            else:
                try:
                    rrd_template += data[p].split(":N:")[0] + ":"
                    rrd_data += data[p].split(":N:")[1] + ":"
                except IndexError:
                    Log("Wrong data format: {0[0]} {0[1]}".format(sys.exc_info()))
                    Log("data[p]: {}".format(data[p]))
                    return

        if data_complete:
            self.update_rrd(RRDFILE, rrd_template, rrd_data)

    def run (self):
        self._running = True
        while self._running:
            self.rrd_particulates()

            for _ in range(500):  # interruptible sleep
                if not self._running:
                    break
                time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# shutdown ####################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    to_rrd.stop()
    to_rrd.join()
    udp.stop()
    udp.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# main ########################################################################
if __name__ == '__main__':
    shutdown_app = Shutdown(shutdown_func=shutdown_application)

    udp = UDP_Receiver()
    to_rrd = ToRRD()

    udp.start()
    to_rrd.start()

    while True:
        time.sleep(120)

# eof #

