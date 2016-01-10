#!/usr/bin/python

import signal
import socket
import sys
from time import strftime, localtime, sleep
from threading import Lock
import traceback

from SensorQueue import SensorQueueClient_write
from SensorValue import SensorValue, SensorValueLock



def Log (logstr):
    """improved log output"""
    print strftime("%Y%m%d %H:%M:%S", localtime()), logstr


class Sensor (object):   # eg DS1820
    def __init__ (self, value, sensorvalue=None):
        self.__value = "%f@%s" % (value, socket.gethostname())
        self.__sv = sensorvalue

    def read (self):
        value = self.__value
        if self.__sv is not None:
            print("schreibe value")
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
    sensor1 = Sensor(17.0, sv1)
    sensor2 = Sensor(45.3, sv2)

    while (True):
        value = sensor1.read()
        Log("client1, sensor1, value = sensor1.read(): %s" % value)
        value = sensor2.read()
        Log("client1, sensor2, value = sensor2.read(): %s" % value)

        for _ in range(25):
            sleep(1)


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)
    sv1 = SensorValueLock("ID_01", "TempWohnzimmer", "temp", Lock())
    sv2 = SensorValueLock("ID_02", "HumiWohnzimmer", "humi", Lock())
    print("vor SensorQueueClient_write")
    sq = SensorQueueClient_write()
    print("nach SensorQueueClient_write")
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

