#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                   #
###############################################################################
"""
"""

### usage ####
# 


import configparser as cfgparser
import rrdtool
import socket
import sys
import threading
import time

sys.path.append('../libs')

from Commons import Digest
from Logging import Log
from Shutdown import Shutdown


CREDENTIALS = "/home/pi/configs/seti.cred"
RRDFILE     = "/schild/weather/seti.rrd"


# Hosts where this app runs
seti_01 = "seti_01"
seti_02 = "seti_02"
seti_03 = "seti_03"
seti_04 = "seti_04"
PIs = [seti_01, seti_02, seti_03, seti_04]
data = { p: None for p in PIs }


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

        self._running = True

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
        # Log("Data: {}".format(data))

    def run (self):
        while self._running:
            try:
                datagram = self.socket.recv(self.MAX_PACKET_SIZE).decode('utf-8')
                # Log("Received: {}".format(datagram))
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

        self.TEMPCPU     = "DS_TEMPCPU"
        self.LOAD        = "DS_LOAD"
        self.FREQ        = "DS_FREQ"
        self.CPU_USE0    = "DS_CPU_USE0"
        self.CPU_USE1    = "DS_CPU_USE1"
        self.CPU_USE2    = "DS_CPU_USE2"
        self.CPU_USE3    = "DS_CPU_USE3"
        self.TEMPROOM    = "DS_TEMPROOM"
        self.TEMPAIRFLOW = "DS_TEMPAIRFLOW"
        self.HUMIDITY    = "DS_HUMIDITY"
        self.RES0        = "DS_RES0"
        self.RES1        = "DS_RES1"
        self.RES2        = "DS_RES2"

        self.DS = { seti_01: { self.TEMPCPU:     '1_tempcpu',
                               self.LOAD:        '1_load',
                               self.FREQ:        '1_freq',
                               self.CPU_USE0:    '1_cpu_use0',
                               self.CPU_USE1:    '1_cpu_use1',
                               self.CPU_USE2:    '1_cpu_use2',
                               self.CPU_USE3:    '1_cpu_use3',
                               self.TEMPROOM:    '1_temproom',
                               self.TEMPAIRFLOW: '1_tempairflow',
                               self.HUMIDITY:    '1_humidity',
                               self.RES0:        '1_res0',
                               self.RES1:        '1_res1',
                               self.RES2:        '1_res2' },
                    seti_02: { self.TEMPCPU:     '2_tempcpu',
                               self.LOAD:        '2_load',
                               self.FREQ:        '2_freq',
                               self.CPU_USE0:    '2_cpu_use0',
                               self.CPU_USE1:    '2_cpu_use1',
                               self.CPU_USE2:    '2_cpu_use2',
                               self.CPU_USE3:    '2_cpu_use3',
                               self.TEMPROOM:    '2_temproom',
                               self.TEMPAIRFLOW: '2_tempairflow',
                               self.HUMIDITY:    '2_humidity',
                               self.RES0:        '2_res0',
                               self.RES1:        '2_res1',
                               self.RES2:        '2_res2' },
                    seti_03: { self.TEMPCPU:     '3_tempcpu',
                               self.LOAD:        '3_load',
                               self.FREQ:        '3_freq',
                               self.CPU_USE0:    '3_cpu_use0',
                               self.CPU_USE1:    '3_cpu_use1',
                               self.CPU_USE2:    '3_cpu_use2',
                               self.CPU_USE3:    '3_cpu_use3',
                               self.TEMPROOM:    '3_temproom',
                               self.TEMPAIRFLOW: '3_tempairflow',
                               self.HUMIDITY:    '3_humidity',
                               self.RES0:        '3_res0',
                               self.RES1:        '3_res1',
                               self.RES2:        '3_res2' },
                    seti_04: { self.TEMPCPU:     '4_tempcpu',
                               self.LOAD:        '4_load',
                               self.FREQ:        '4_freq',
                               self.CPU_USE0:    '4_cpu_use0',
                               self.CPU_USE1:    '4_cpu_use1',
                               self.CPU_USE2:    '4_cpu_use2',
                               self.CPU_USE3:    '4_cpu_use3',
                               self.TEMPROOM:    '4_temproom',
                               self.TEMPAIRFLOW: '4_tempairflow',
                               self.HUMIDITY:    '4_humidity',
                               self.RES0:        '4_res0',
                               self.RES1:        '4_res1',
                               self.RES2:        '4_res2' }
                  }

        self._running = True

    def run (self):
        while self._running:
            data_complete = True
            rrd_template = ""
            rrd_data = "N:"

            for p in PIs:
                if not data[p]:
                    data_complete = False
                else:    
                    rrd_template = rrd_template + self.DS[p][self.TEMPCPU]     + ":" + \
                                                  self.DS[p][self.LOAD]        + ":" + \
                                                  self.DS[p][self.FREQ]        + ":" + \
                                                  self.DS[p][self.CPU_USE0]    + ":" + \
                                                  self.DS[p][self.CPU_USE1]    + ":" + \
                                                  self.DS[p][self.CPU_USE2]    + ":" + \
                                                  self.DS[p][self.CPU_USE3]    + ":" + \
                                                  self.DS[p][self.TEMPROOM]    + ":" + \
                                                  self.DS[p][self.TEMPAIRFLOW] + ":" + \
                                                  self.DS[p][self.HUMIDITY]    + ":" + \
                                                  self.DS[p][self.RES0]        + ":" + \
                                                  self.DS[p][self.RES1]        + ":" + \
                                                  self.DS[p][self.RES2]        + ":"
                    rrd_data = rrd_data + data[p].split("N:")[1].rstrip() + ":"

            if data_complete:
                rrd_template = rrd_template.rstrip(":")
                rrd_data     = rrd_data.rstrip(":")
                                                                
                Log(rrd_template)
                Log(rrd_data)
                rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)

            for _ in range(600):  # interruptible sleep
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

