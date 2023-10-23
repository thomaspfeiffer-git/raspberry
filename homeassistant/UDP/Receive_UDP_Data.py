#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Receive_UDP_Data.py                                                         #
# (c) https://github.com/thomaspfeiffer-git 2023                              #
###############################################################################

"""
TODO
"""


"""
###### Usage ######
nohup ./Receive_UDP_Data.py 2>1 > receive_udp_data.log &
"""


import os
import sys

sys.path.append("../../libs/")
from Logging import Log
from Shutdown import Shutdown
import UDP


CREDENTIALS = os.path.expanduser("~/credentials/homeautomation.cred")


"""
    from SensorQueue2 import SensorQueueClient_write
    from SensorValue2 import SensorValue, SensorValue_Data

    qv_temp_wardrobe  = SensorValue("ID_31", "TempWardrobe",  SensorValue_Data.Types.Temp, "°C")
    qv_humi_wardrobe  = SensorValue("ID_32", "HumiWardrobe",  SensorValue_Data.Types.Humi, "% rF")
    qv_light_wardrobe = SensorValue("ID_33", "LightWardrobe", SensorValue_Data.Types.Light, "lux")

    sq = SensorQueueClient_write("../../configs/weatherqueue.ini")
    sq.register(qv_temp_wardrobe)
    sq.register(qv_humi_wardrobe)
    sq.register(qv_light_wardrobe)

    lightness = Lightness(qv=qv_light_wardrobe)
    htu21df = HTU21DF(qvalue_temp=qv_temp_wardrobe, qvalue_humi=qv_humi_wardrobe)


    if self.__qvalue_temp is not None:
        self.__qvalue_temp.value = "%.1f" % (t)
"""



###############################################################################
# Receiver ####################################################################
class Receiver (object):
    def __init__ (self):
        self.udp = UDP.Receiver(CREDENTIALS)

    def start (self):
        while True:
            payload = self.udp.receive()
            try:
                source = payload.split(" - ")[0]
                data = payload.split(" - ")[1]
            except IndexError:
                Log("Wrong data format: {0[0]} {0[1]}".format(sys.exc_info()))
            else:
                Log(f"Source: {source}; Data: {data}")


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    r = Receiver()
    r.start()

# eof #

