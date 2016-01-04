#!/usr/bin/python

import signal
import sys
from time import strftime, localtime, sleep
from threading import Lock
import traceback

from SensorQueue import SensorQueueClient
from SensorValue import SensorValue, SensorValueLock



def Log (logstr):
    """improved log output"""
    print strftime("%Y%m%d %H:%M:%S", localtime()), logstr


class Sensor (object):   # eg DS1820
    def __init__ (self, sensorvalue=None):
        self.__sv = sensorvalue

    def read (self):
        value = 22.2
        if self.__sv is not None:
            self.__sv.value = value 
        return value



###############################################################################
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    sq.stop()
    sq.join()
    print("Exit")
    sys.exit()

def _Exit(__s, __f):
    """exit for signal handler"""
    print("_Exit")
    Exit()


###############################################################################
# Main ########################################################################
def Main():
    sensor1 = Sensor(sv1)
    sensor2 = Sensor(sv2)

    while (True):
        value = sensor1.read()
        Log("client1, sensor1, value = sensor1.read(): %s" % value)
        value = sensor2.read()
        Log("client1, sensor2, value = sensor2.read(): %s" % value)
        sleep(25)


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)
    sv1 = SensorValueLock("TempWohnzimmer", "temp", Lock())
    sv2 = SensorValueLock("HumiWohnzimmer", "humi", Lock())
    sq = SensorQueueClient()
    sq.register(sv1)
    sq.register(sv2)
    sq.start()

    try:
        Main()

    except KeyboardInterrupt:
        Exit()

    except SystemExit:                  # Done in signal handler (method _Exit()) #
        pass

    except:
        print(traceback.print_exc())

    finally:        # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

# eof #

