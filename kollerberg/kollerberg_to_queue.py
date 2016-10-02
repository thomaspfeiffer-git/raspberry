#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# kollerberg_to_queue.py                                                      #
# Copies data from Kollerberg's data files to the queue used for the local    #
# weather station.                                                            #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################


import signal
import sys
from threading import Lock
from time import sleep
import traceback

sys.path.append('../libs')
from SensorQueue import SensorQueueClient_write
from SensorValue import SensorValueLock, SensorValue



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
    qv_kb_i_t = SensorValueLock("ID_2?", "Temp KB indoor", SensorValue.Types.Temp, u'°C', Lock())
    qv_kb_i_h = SensorValueLock("ID_2?", "Humi KB indoor", SensorValue.Types.Humi, u'% rF', Lock())
    qv_kb_p   = SensorValueLock("ID_2?", "Pressure KB",    SensorValue.Types.Pressure, u'hPa', Lock())

    qv_kb_a_t = SensorValueLock("ID_2?", "Temp KB outdoor", SensorValue.Types.Temp, u'°C', Lock())
    qv_kb_a_h = SensorValueLock("ID_2?", "Humi KB outdoor", SensorValue.Types.Humi, u'% rF', Lock())

    qv_kb_k_t = SensorValueLock("ID_2?", "Temp KB basement", SensorValue.Types.Temp, u'°C', Lock())
    qv_kb_k_h = SensorValueLock("ID_2?", "Humi KB basement", SensorValue.Types.Humi, u'% rF', Lock())


    sq.register(qvalue_temp)
    sq.register(qvalue_humi)
    sq.start()


    while True:
        # read data from files:
        #   ID_21: temp outdoor
        #   ID_22: humi outdoor
        #   ID_23: air pressure
        #   ID_24: temp indoor
        #   ID_25: humi indoor
        #   ID_26: temp basement
        #   ID_27: humi basement

        # write data into queue

        data = getDataFromFile(DATAFILES[pik_i])
        kb_i_t = data[3]
        kb_i_h = data[6]
        kb_i_p = data[7]

        data = getDataFromFile(DATAFILES[pik_a])
        kb_a_t = data[3]
        kb_a_h = data[6]

        data = getDataFromFile(DATAFILES[pik_k])
        kb_k_t = data[3]
        kb_k_h = data[6]


        sleep(60)



################################################################################
# Exit ########################################################################
def Exit():
    """cleanup stuff"""
    sq.stop()
    sq.join()
    sys.exit()

def _Exit(__s, __f):
    """cleanup stuff used for signal handler"""
    Exit()


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)

    try:
        sq = SensorQueueClient_write()
        Main()

    except KeyboardInterrupt:
        Exit()

    except SystemExit:              # Done in signal handler (method _Exit()) #
        pass

    except:
        print(traceback.print_exc())

    finally:
        pass

# eof #

