#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# kollerberg_to_queue.py                                                      #
# Copies data from Kollerberg's data files to the queue used for the local    #
# weather station.                                                            #
# (c) https://github.com/thomaspfeiffer-git 2016, 2017                        #
###############################################################################

# start width
# nohup ./kollerberg_to_queue.py 2>kollerberg_to_queue.err > kollerberg_to_queue.log &

import sys
from time import sleep
import traceback

sys.path.append('../libs')
from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data
from Shutdown import Shutdown


pik_i = "pik_i"
pik_a = "pik_a"
pik_k = "pik_k"
PIs = [pik_i, pik_a, pik_k]

DATAFILES = { pik_i: "/schild/weather/kb_i_weather.data",
              pik_a: "/schild/weather/kb_a_weather.data",
              pik_k: "/schild/weather/kb_k_weather.data" }


def getDataFromFile (filename):
    with open(filename, 'r') as f:
        return f.read().split(':')


################################################################################
# Main #########################################################################
def Main():
    qv_kb_i_t = SensorValue("ID_21", "Temp KB indoor", SensorValue_Data.Types.Temp, "°C")
    qv_kb_i_h = SensorValue("ID_22", "Humi KB indoor", SensorValue_Data.Types.Humi, "% rF")
    qv_kb_p   = SensorValue("ID_23", "Pressure KB",    SensorValue_Data.Types.Pressure, "hPa")

    qv_kb_a_t = SensorValue("ID_24", "Temp KB outdoor", SensorValue_Data.Types.Temp, "°C")
    qv_kb_a_h = SensorValue("ID_25", "Humi KB outdoor", SensorValue_Data.Types.Humi, "% rF")

    qv_kb_k_t = SensorValue("ID_26", "Temp KB basement", SensorValue_Data.Types.Temp, "°C")
    qv_kb_k_h = SensorValue("ID_27", "Humi KB basement", SensorValue_Data.Types.Humi, "% rF")

    sq.register(qv_kb_i_t)
    sq.register(qv_kb_i_h)
    sq.register(qv_kb_p)
    sq.register(qv_kb_a_t)
    sq.register(qv_kb_a_h)
    sq.register(qv_kb_k_t)
    sq.register(qv_kb_k_h)

    while True:
        try:
            data = getDataFromFile(DATAFILES[pik_i])
            print("pik_i", data)
            qv_kb_i_t.value = "%.1f" % (float(data[3]))  # convert from nn,nn to nn,n
            qv_kb_i_h.value = "%.1f" % (float(data[6]))
            qv_kb_p.value   = "%.1f" % (float(data[7]))

            data = getDataFromFile(DATAFILES[pik_a])
            print("pik_a", data)
            qv_kb_a_t.value = "%.1f" % (float(data[3]))
            qv_kb_a_h.value = "%.1f" % (float(data[6]))

            data = getDataFromFile(DATAFILES[pik_k])
            print("pik_k", data)
            qv_kb_k_t.value = "%.1f" % (float(data[3]))
            qv_kb_k_h.value = "%.1f" % (float(data[6]))
        except (IndexError, ValueError):  # access to data files is not synchronized,
            pass                          # thus data[] can be an empty array.

        sleep(60)


################################################################################
# Exit #########################################################################
def shutdown_application ():
    """cleanup stuff"""
    sys.exit(0)


###############################################################################
###############################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    sq = SensorQueueClient_write("../../configs/weatherqueue.ini")
    Main()

# eof #

