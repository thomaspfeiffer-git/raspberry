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


###############################################################################
### TODO ######################################################################
# Weather_Kollerberg.py --> Receiver_Homeautomation



import os
import sys

sys.path.append("../../libs/")
from Logging import Log
from Shutdown import Shutdown
import UDP


### TODO: move to local directory ./
from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data

CREDENTIALS = os.path.expanduser("~/credentials/homeautomation.cred")


###############################################################################
# SQ ##########################################################################
class SQ (SensorQueueClient_write):
    def __init__ (self):
        ### TODO change path ###
        super().__init__("../../../configs_2_delete/weatherqueue.ini")


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
                cls = globals()[source.lower()]
                cls.update(data)


###############################################################################
# Wardrobe ####################################################################
class Wardrobe (object):
    def __init__ (self):
        self.qv_temp  = SensorValue("XID_31", "TempWardrobe", SensorValue_Data.Types.Temp, "°C")
        self.qv_humi  = SensorValue("XID_32", "HumiWardrobe", SensorValue_Data.Types.Humi, "% rF")
        self.qv_light = SensorValue("XID_33", "LightWardrobe", SensorValue_Data.Types.Light, "lux")

        self.sq = SQ()
        self.sq.register(self.qv_temp)
        self.sq.register(self.qv_humi)
        self.sq.register(self.qv_light)

    def update (self, rrd):
        ### TODO validate data
        items = rrd.split(":")
        temp = float(items[1])
        humi = float(items[2])
        light = float(items[4])
        self.set_values(temp, humi, light)

    def set_values (self, temp, humi, light):
        self.qv_temp.value = f"{temp:.1f}"
        self.qv_humi.value = f"{humi:.1f}"
        self.qv_light.value = f"{light:.1f}"


###############################################################################
# Serverroom ##################################################################
class Serverroom (object):
    def __init__ (self):
        self.qv_temp  = SensorValue("XID_98", "TempServerroom", SensorValue_Data.Types.Temp, "°C")
        self.qv_humi  = SensorValue("XID_99", "HumiServerroom", SensorValue_Data.Types.Humi, "% rF")

        self.sq = SQ()
        self.sq.register(self.qv_temp)
        self.sq.register(self.qv_humi)

    def update (self, rrd):
        ### TODO validate data
        items = rrd.split(":")
        temp = float(items[1])
        humi = float(items[2])
        self.set_values(temp, humi)

    def set_values (self, temp, humi):
        self.qv_temp.value = f"{temp:.1f}"
        self.qv_humi.value = f"{humi:.1f}"


###############################################################################
# Power #######################################################################
class Power (object):
    def __init__ (self):
        self.qv_power  = SensorValue("P_ID_01", "MainPower", SensorValue_Data.Types.Power, "W")

        self.sq = SQ()
        self.sq.register(self.qv_power)

    def update (self, rrd):
        ### TODO validate data
        items = rrd.split(":")
        power = float(items[18])
        self.set_values(power)

    def set_values (self, power):
        self.qv_power.value = f"{power:.1f}"


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
    wardrobe = Wardrobe()
    serverroom = Serverroom()
    power = Power()

    r = Receiver()
    r.start()

# eof #

