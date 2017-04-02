#!/usr/bin/python3
"""provides fake data to the QueueServer2 for testing purposes"""

import random
import sys
import time
import threading

sys.path.append("../../libs/")
from SensorQueue2 import SensorQueueClient_write
from SensorValue import SensorValueLock, SensorValue
from Shutdown import Shutdown


def shutdown_application ():
    """called on shutdown; stops all threads"""
    print("in shutdown_application")
    sq.stop()
    sq.join()
    sys.exit(0)


# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    qv = {
          'qv_temp_wardrobe': SensorValueLock("ID_31", "TempWardrobe", SensorValue.Types.Temp, "°C", threading.Lock()),
          'qv_humi_wardrobe': SensorValueLock("ID_32", "HumiWardrobe", SensorValue.Types.Humi, "% rF", threading.Lock()),
          'qv_light_wardrobe': SensorValueLock("ID_33", "LightWardrobe", SensorValue.Types.Light, "lux", threading.Lock()),
          'qvalue_temp_indoor':      SensorValueLock("ID_01", "TempWohnzimmerIndoor", SensorValue.Types.Temp, "°C", threading.Lock()),
          'qvalue_humi_indoor':      SensorValueLock("ID_02", "HumiWohnzimmerIndoor", SensorValue.Types.Humi, "% rF", threading.Lock()),
          'qvalue_temp_outdoor':     SensorValueLock("ID_03", "TempWohnzimmerOutdoor", SensorValue.Types.Temp, "°C", threading.Lock()),
          'qvalue_humi_outdoor':     SensorValueLock("ID_04", "HumiWohnzimmerOutdoor", SensorValue.Types.Humi, "% rF", threading.Lock()),
          'qvalue_pressure':         SensorValueLock("ID_05", "Luftdruck", SensorValue.Types.Pressure, "hPa", threading.Lock()),
          'qvalue_temp_realoutdoor': SensorValueLock("ID_12", "TempRealOutdoor", SensorValue.Types.Temp, "°C", threading.Lock()),
          'qvalue_temp_indoor2':     SensorValueLock("ID_13", "TempWohnzimmerFenster", SensorValue.Types.Temp, "°C", threading.Lock())
         }

    sq = SensorQueueClient_write("../config.ini")
    list(map(sq.register, qv.values()))
    sq.start()

    while True:
        print("sending values ...")
        qv['qv_temp_wardrobe'].value = "22.{:02d}".format(random.randint(0,99))
        qv['qv_humi_wardrobe'].value = "67.{:02d}".format(random.randint(0,99))
        qv['qv_light_wardrobe'].value = "823.{:02d}".format(random.randint(0,99))
        qv['qvalue_temp_indoor'].value = "11.{:02d}".format(random.randint(0,99))
        qv['qvalue_humi_indoor'].value = "11.{:02d}".format(random.randint(0,99))
        qv['qvalue_temp_outdoor'].value = "22.{:02d}".format(random.randint(0,99))
        qv['qvalue_humi_outdoor'].value = "22.{:02d}".format(random.randint(0,99))
        qv['qvalue_pressure'].value = "1013.{:02d}".format(random.randint(0,99))
        qv['qvalue_temp_realoutdoor'].value = "-22.{:02d}".format(random.randint(0,99))
        qv['qvalue_temp_indoor2'].value = "23.{:02d}".format(random.randint(0,99))
        time.sleep(45)

# eof #

