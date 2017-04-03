#!/usr/bin/python3
"""provides fake data to the QueueServer2 for testing purposes"""

import random
import sys
import time

sys.path.append("../../libs/")
from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data
from Shutdown import Shutdown


def shutdown_application ():
    """called on shutdown; stops all threads"""
    print("in shutdown_application")
    sys.exit(0)


# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    qv = {
          'qv_temp_wardrobe':    SensorValue("ID_31", "TempWardrobe", SensorValue_Data.Types.Temp, "°C"),
          'qv_humi_wardrobe':    SensorValue("ID_32", "HumiWardrobe", SensorValue_Data.Types.Humi, "% rF"),
          'qv_light_wardrobe':   SensorValue("ID_33", "LightWardrobe", SensorValue_Data.Types.Light, "lux"),
          'qv_temp_indoor':      SensorValue("ID_01", "TempWohnzimmerIndoor", SensorValue_Data.Types.Temp, "°C"),
          'qv_humi_indoor':      SensorValue("ID_02", "HumiWohnzimmerIndoor", SensorValue_Data.Types.Humi, "% rF"),
          'qv_temp_outdoor':     SensorValue("ID_03", "TempWohnzimmerOutdoor", SensorValue_Data.Types.Temp, "°C"),
          'qv_humi_outdoor':     SensorValue("ID_04", "HumiWohnzimmerOutdoor", SensorValue_Data.Types.Humi, "% rF"),
          'qv_pressure':         SensorValue("ID_05", "Luftdruck", SensorValue_Data.Types.Pressure, "hPa"),
          'qv_temp_realoutdoor': SensorValue("ID_12", "TempRealOutdoor", SensorValue_Data.Types.Temp, "°C"),
          'qv_temp_indoor2':     SensorValue("ID_13", "TempWohnzimmerFenster", SensorValue_Data.Types.Temp, "°C")
         }

    sq = SensorQueueClient_write("../config.ini")
    list(map(sq.register, qv.values()))
    # sq.start()

    while True:
        # print("sending values ...")
        qv['qv_temp_wardrobe'].value = "22.{:02d}".format(random.randint(0,99))
        qv['qv_humi_wardrobe'].value = "67.{:02d}".format(random.randint(0,99))
        qv['qv_light_wardrobe'].value = "823.{:02d}".format(random.randint(0,99))
        qv['qv_temp_indoor'].value = "11.{:02d}".format(random.randint(0,99))
        qv['qv_humi_indoor'].value = "11.{:02d}".format(random.randint(0,99))
        qv['qv_temp_outdoor'].value = "22.{:02d}".format(random.randint(0,99))
        qv['qv_humi_outdoor'].value = "22.{:02d}".format(random.randint(0,99))
        qv['qv_pressure'].value = "1013.{:02d}".format(random.randint(0,99))
        qv['qv_temp_realoutdoor'].value = "-22.{:02d}".format(random.randint(0,99))
        qv['qv_temp_indoor2'].value = "23.{:02d}".format(random.randint(0,99))
        time.sleep(5)

# eof #

