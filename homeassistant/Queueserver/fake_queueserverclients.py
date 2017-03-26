#!/usr/bin/python3
"""provides fake data to the QueueServer2 for testing purposes"""

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
          'qv_light_wardrobe': SensorValueLock("ID_33", "LightWardrobe", SensorValue.Types.Light, "lux", threading.Lock())
         }

    sq = SensorQueueClient_write()
    # map(sq.register, qv.values())
    sq.register(qv['qv_temp_wardrobe'])
    sq.register(qv['qv_humi_wardrobe'])
    sq.register(qv['qv_light_wardrobe'])
    sq.start()

    while True:
        print("sending values ...")
        qv['qv_temp_wardrobe'].value = "22.2"
        # qv['qv_humi_wardrobe'].value = "67.3"
        # qv['qv_light_wardrobe'].value = "823"
        time.sleep(45)

# eof #

