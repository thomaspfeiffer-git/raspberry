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
          'qv_temp_kid':         SensorValue("ID_06", "TempKinderzimmer", SensorValue_Data.Types.Temp, "°C"),
          'qv_humi_kid':         SensorValue("ID_07", "HumiKinderzimmer", SensorValue_Data.Types.Humi, "% rF"),
          'qv_temp_realoutdoor': SensorValue("ID_12", "TempRealOutdoor", SensorValue_Data.Types.Temp, "°C"),
          'qv_temp_indoor2':     SensorValue("ID_13", "TempWohnzimmerFenster", SensorValue_Data.Types.Temp, "°C"),

          'qv_kb_i_t': SensorValue("ID_21", "Temp KB indoor", SensorValue_Data.Types.Temp, "°C"),
          'qv_kb_i_h': SensorValue("ID_22", "Humi KB indoor", SensorValue_Data.Types.Humi, "% rF"),
          'qv_kb_p':   SensorValue("ID_23", "Pressure KB",    SensorValue_Data.Types.Pressure, "hPa"),
          'qv_kb_a_t': SensorValue("ID_24", "Temp KB outdoor", SensorValue_Data.Types.Temp, "°C"),
          'qv_kb_a_h': SensorValue("ID_25", "Humi KB outdoor", SensorValue_Data.Types.Humi, "% rF"),
          'qv_kb_k_t': SensorValue("ID_26", "Temp KB basement", SensorValue_Data.Types.Temp, "°C"),
          'qv_kb_k_h': SensorValue("ID_27", "Humi KB basement", SensorValue_Data.Types.Humi, "% rF")
         }


    for i in range(3):
        qv.update({'temp_owm_{}'.format(i): SensorValue("ID_OWM_{}1".format(i), "TempOWM_{}".format(i), SensorValue_Data.Types.Temp, "°C"),
                   'humidity_owm_{}'.format(i): SensorValue("ID_OWM_{}2".format(i), "HumiOWM_{}".format(i), SensorValue_Data.Types.Humi, "% rF"),
                   'wind_owm_{}'.format(i): SensorValue("ID_OWM_{}3".format(i), "WindOWM_{}".format(i), SensorValue_Data.Types.Wind, "km/h"),
                   'wind direction_owm_{}'.format(i): SensorValue("ID_OWM_{}4".format(i), "WindDirOWM_{}".format(i), SensorValue_Data.Types.WindDir, None),
                   'desc_owm_{}'.format(i): SensorValue("ID_OWM_{}5".format(i), "DescOWM_{}".format(i), SensorValue_Data.Types.Desc, None),
                   })



    sq = SensorQueueClient_write("../config.ini")
    list(map(sq.register, qv.values()))
    # sq.start()

    while True:
        # print("sending values ...")
        qv['qv_temp_wardrobe'].value = "55.{:02d}".format(random.randint(0,99))
        qv['qv_humi_wardrobe'].value = "56.{:02d}".format(random.randint(0,99))
        qv['qv_light_wardrobe'].value = "823.{:02d}".format(random.randint(0,99))
        qv['qv_temp_indoor'].value = "11.{:02d}".format(random.randint(0,99))
        qv['qv_humi_indoor'].value = "12.{:02d}".format(random.randint(0,99))
        qv['qv_temp_outdoor'].value = "22.{:02d}".format(random.randint(0,99))
        qv['qv_humi_outdoor'].value = "23.{:02d}".format(random.randint(0,99))
        qv['qv_pressure'].value = "1013.{:01d}".format(random.randint(0,9))
        qv['qv_temp_kid'].value = "33.{:02d}".format(random.randint(0,99))
        qv['qv_humi_kid'].value = "34.{:02d}".format(random.randint(0,99))
        qv['qv_temp_realoutdoor'].value = "-22.{:02d}".format(random.randint(0,99))
        qv['qv_temp_indoor2'].value = "23.{:02d}".format(random.randint(0,99))

        qv['qv_kb_i_t'].value = "66.{:02d}".format(random.randint(0,99))
        qv['qv_kb_i_h'].value = "67.{:02d}".format(random.randint(0,99))
        qv['qv_kb_p'].value = "1068.{:01d}".format(random.randint(0,9))
        qv['qv_kb_a_t'].value = "77.{:02d}".format(random.randint(0,99))
        qv['qv_kb_a_h'].value = "78.{:02d}".format(random.randint(0,99))
        qv['qv_kb_k_t'].value = "88.{:02d}".format(random.randint(0,99))
        qv['qv_kb_k_h'].value = "89.{:02d}".format(random.randint(0,99))

        qv['temp_owm_0'].value = "22.{:01d}".format(random.randint(0,9))
        qv['humidity_owm_0'].value = "23.{:01d}".format(random.randint(0,9))
        qv['wind_owm_0'].value = "24.{:01d}".format(random.randint(0,9))
        qv['wind direction_owm_0'].value = "nordwest"
        qv['desc_owm_0'].value = "leicht bewölkt"

        qv['temp_owm_1'].value = "32.{:01d}".format(random.randint(0,9))
        qv['humidity_owm_1'].value = "33.{:01d}".format(random.randint(0,9))
        qv['wind_owm_1'].value = "34.{:01d}".format(random.randint(0,9))
        qv['wind direction_owm_1'].value = "west"
        qv['desc_owm_1'].value = "starke Sonne"

        qv['temp_owm_2'].value = "42.{:01d}".format(random.randint(0,9))
        qv['humidity_owm_2'].value = "43.{:01d}".format(random.randint(0,9))
        qv['wind_owm_2'].value = "44.{:01d}".format(random.randint(0,9))
        qv['wind direction_owm_2'].value = "südost"
        qv['desc_owm_2'].value = "leichter Regen"

        time.sleep(1)

# eof #

