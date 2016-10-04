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
    qv_kb_i_t = SensorValueLock("ID_21", "Temp KB indoor", SensorValue.Types.Temp, u'°C', Lock())
    qv_kb_i_h = SensorValueLock("ID_22", "Humi KB indoor", SensorValue.Types.Humi, u'% rF', Lock())
    qv_kb_p   = SensorValueLock("ID_23", "Pressure KB",    SensorValue.Types.Pressure, u'hPa', Lock())

    qv_kb_a_t = SensorValueLock("ID_24", "Temp KB outdoor", SensorValue.Types.Temp, u'°C', Lock())
    qv_kb_a_h = SensorValueLock("ID_25", "Humi KB outdoor", SensorValue.Types.Humi, u'% rF', Lock())

    qv_kb_k_t = SensorValueLock("ID_26", "Temp KB basement", SensorValue.Types.Temp, u'°C', Lock())
    qv_kb_k_h = SensorValueLock("ID_27", "Humi KB basement", SensorValue.Types.Humi, u'% rF', Lock())

    sq.register(qv_kb_i_t)
    sq.register(qv_kb_i_h)
    sq.register(qv_kb_p)
    sq.register(qv_kb_a_t)
    sq.register(qv_kb_a_h)
    sq.register(qv_kb_k_t)
    sq.register(qv_kb_k_h)
    sq.start()

    while True:
        try:
            data = getDataFromFile(DATAFILES[pik_i])
            qv_kb_i_t.value = "%.1f" % (float(data[3]))  # convert from nn,nn to nn,n
            qv_kb_i_h.value = "%.1f" % (float(data[6]))
            qv_kb_p.value   = "%.1f" % (float(data[7]))

            data = getDataFromFile(DATAFILES[pik_a])
            qv_kb_a_t.value = "%.1f" % (float(data[3]))
            qv_kb_a_h.value = "%.1f" % (float(data[6]))

            data = getDataFromFile(DATAFILES[pik_k])
            qv_kb_k_t.value = "%.1f" % (float(data[3]))
            qv_kb_k_h.value = "%.1f" % (float(data[6]))
        except IndexError:  # access to data files is not synchronized,
            pass            # thus data[] can be an empty array.

        sleep(60)


################################################################################
# Exit #########################################################################
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

