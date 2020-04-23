#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Seti_UDP.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2020                   #
###############################################################################
"""
TODO
"""

"""
### usage ###
TODO
"""

import os
import rrdtool
import sys

sys.path.append('../libs')

from Logging import Log
from Shutdown import Shutdown
import UDP


CREDENTIALS = os.path.expanduser("~/credentials/seti.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/seti.rrd")

# Hosts where this app runs
seti_01 = "seti-01"
seti_02 = "seti-02"
seti_03 = "seti-03"
seti_04 = "seti-04"
PIs = [seti_01, seti_02, seti_03, seti_04]


###############################################################################
# RRD #########################################################################
class RRD (object):
    TEMPCPU     = "DS_TEMPCPU"
    LOAD        = "DS_LOAD"
    FREQ        = "DS_FREQ"
    CPU_USE0    = "DS_CPU_USE0"
    CPU_USE1    = "DS_CPU_USE1"
    CPU_USE2    = "DS_CPU_USE2"
    CPU_USE3    = "DS_CPU_USE3"
    TEMPROOM    = "DS_TEMPROOM"
    TEMPAIRFLOW = "DS_TEMPAIRFLOW"
    HUMIDITY    = "DS_HUMIDITY"
    RES0        = "DS_RES0"
    RES1        = "DS_RES1"
    RES2        = "DS_RES2"

    DS = { seti_01: { TEMPCPU:     '1_tempcpu',
                      LOAD:        '1_load',
                      FREQ:        '1_freq',
                      CPU_USE0:    '1_cpu_use0',
                      CPU_USE1:    '1_cpu_use1',
                      CPU_USE2:    '1_cpu_use2',
                      CPU_USE3:    '1_cpu_use3',
                      TEMPROOM:    '1_temproom',
                      TEMPAIRFLOW: '1_tempairflow',
                      HUMIDITY:    '1_humidity',
                      RES0:        '1_res0',
                      RES1:        '1_res1',
                      RES2:        '1_res2' },
           seti_02: { TEMPCPU:     '2_tempcpu',
                      LOAD:        '2_load',
                      FREQ:        '2_freq',
                      CPU_USE0:    '2_cpu_use0',
                      CPU_USE1:    '2_cpu_use1',
                      CPU_USE2:    '2_cpu_use2',
                      CPU_USE3:    '2_cpu_use3',
                      TEMPROOM:    '2_temproom',
                      TEMPAIRFLOW: '2_tempairflow',
                      HUMIDITY:    '2_humidity',
                      RES0:        '2_res0',
                      RES1:        '2_res1',
                      RES2:        '2_res2' },
           seti_03: { TEMPCPU:     '3_tempcpu',
                      LOAD:        '3_load',
                      FREQ:        '3_freq',
                      CPU_USE0:    '3_cpu_use0',
                      CPU_USE1:    '3_cpu_use1',
                      CPU_USE2:    '3_cpu_use2',
                      CPU_USE3:    '3_cpu_use3',
                      TEMPROOM:    '3_temproom',
                      TEMPAIRFLOW: '3_tempairflow',
                      HUMIDITY:    '3_humidity',
                      RES0:        '3_res0',
                      RES1:        '3_res1',
                      RES2:        '3_res2' },
           seti_04: { TEMPCPU:     '4_tempcpu',
                      LOAD:        '4_load',
                      FREQ:        '4_freq',
                      CPU_USE0:    '4_cpu_use0',
                      CPU_USE1:    '4_cpu_use1',
                      CPU_USE2:    '4_cpu_use2',
                      CPU_USE3:    '4_cpu_use3',
                      TEMPROOM:    '4_temproom',
                      TEMPAIRFLOW: '4_tempairflow',
                      HUMIDITY:    '4_humidity',
                      RES0:        '4_res0',
                      RES1:        '4_res1',
                      RES2:        '4_res2' }
         }

    def __init__ (self):
        self.data = { p: None for p in PIs }

    def process (self):
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

                Log(rrd_data)
                try:
                    rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)
                except rrdtool.OperationalError:
                    Log("Cannot update rrd database: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
# Receiver ####################################################################
class Receiver (object):
    def __init__ (self):
        self.udp = UDP.Receiver(CREDENTIALS)
        self.rrd = RRD()

    def run (self):
        while True:
            payload = self.udp.receive()
            (source, values) = payload.split(',')
            self.rrd.data[source] = values
            self.rrd.process()


###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    r = Receiver()
    r.run()

# eof #

