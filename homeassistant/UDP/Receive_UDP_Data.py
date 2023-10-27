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

sys.path.append("../Queueserver/")
from SensorQueue import SensorQueueClient_write
from SensorValue import SensorValue, SensorValue_Data

CREDENTIALS = os.path.expanduser("~/credentials/homeautomation.cred")


###############################################################################
# SQ ##########################################################################
class SQ (SensorQueueClient_write):
    def __init__ (self):
        super().__init__("../config.ini")


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
                Log("Wrong data format: {0[0]} {0[1]}".format(sys.exc_info()), sys.stderr)
            else:
                try:
                    cls = globals()[source.lower()]
                except KeyError:
                    Log(f"No class/object '{source.lower()}' instantiated.", sys.stderr)
                else:
                    cls.update(data)


###############################################################################
# Wardrobe ####################################################################
class Wardrobe (object):
    def __init__ (self):
        self.qv_temp  = SensorValue("ID_31", "TempWardrobe", SensorValue_Data.Types.Temp, "°C")
        self.qv_humi  = SensorValue("ID_32", "HumiWardrobe", SensorValue_Data.Types.Humi, "% rF")
        self.qv_light = SensorValue("ID_33", "LightWardrobe", SensorValue_Data.Types.Light, "lux")

        self.sq = SQ()
        self.sq.register(self.qv_temp)
        self.sq.register(self.qv_humi)
        self.sq.register(self.qv_light)

    def update (self, rrd):
        ### TODO validate data
        items = rrd.split(":")
        self.qv_temp.value = f"{float(items[1]):.1f}"
        self.qv_humi.value = f"{float(items[2]):.1f}"
        self.qv_light.value = f"{float(items[4]):.1f}"


###############################################################################
# Serverroom ##################################################################
class Serverroom (object):
    def __init__ (self):  ### TODO: Check IDs
        self.qv_temp  = SensorValue("ID_41", "TempServerroom", SensorValue_Data.Types.Temp, "°C")
        self.qv_humi  = SensorValue("ID_42", "HumiServerroom", SensorValue_Data.Types.Humi, "% rF")

        self.sq = SQ()
        self.sq.register(self.qv_temp)
        self.sq.register(self.qv_humi)

    def update (self, rrd):
        ### TODO validate data
        items = rrd.split(":")
        self.qv_temp.value = f"{float(items[1]):.1f}"
        self.qv_humi.value = f"{float(items[2]):.1f}"


###############################################################################
# Power #######################################################################
class Power (object):
    def __init__ (self):
        self.qv_power  = SensorValue("ID_50", "MainPower", SensorValue_Data.Types.Power, "W")

        self.sq = SQ()
        self.sq.register(self.qv_power)

    def update (self, rrd):
        ### TODO validate data
        items = rrd.split(":")
        self.qv_power.value = f"{float(items[18]):.1f}"


###############################################################################
# Weater_Outdoor ##############################################################
class Weather_Outdoor (object):
    def __init__ (self):
        self.qv_temp        = SensorValue("ID_03", "TempOutdoor", SensorValue_Data.Types.Temp, "°C")
        self.qv_temp_garden = SensorValue("ID_12", "TempOutdoorGarden", SensorValue_Data.Types.Temp, "°C")
        self.qv_humi        = SensorValue("ID_04", "HumiOutdoor", SensorValue_Data.Types.Humi, "% rF")
        self.qv_lightness   = SensorValue("ID_15", "LightnessOutdoor", SensorValue_Data.Types.Light, "lux")

        self.sq = SQ()
        self.sq.register(self.qv_temp)
        self.sq.register(self.qv_temp_garden)
        self.sq.register(self.qv_humi)
        self.sq.register(self.qv_lightness)

    def update (self, rrd):
        ### TODO validate data
        items = rrd.split(":")
        self.qv_temp.value = f"{float(items[1]):.1f}"
        self.qv_temp_garden.value = f"{float(items[2]):.1f}"
        self.qv_humi.value = f"{float(items[3]):.1f}"
        self.qv_lightness.value = f"{float(items[5]):.1f}"


###############################################################################
# Weather_Indoor ##############################################################
class Weather_Indoor (object):
    def __init__ (self):
        self.qv_temp       = SensorValue("ID_01", "TempWohnzimmerIndoor", SensorValue_Data.Types.Temp, "°C")
        self.qv_humi       = SensorValue("ID_02", "HumiWohnzimmerIndoor", SensorValue_Data.Types.Humi, "% rF")
        self.qv_pressure   = SensorValue("ID_05", "Luftdruck", SensorValue_Data.Types.Pressure, "hPa")
        self.qv_airquality = SensorValue("ID_14", "AirQualityWohnzimmer", SensorValue_Data.Types.AirQuality, "%")

        self.sq = SQ()
        self.sq.register(self.qv_temp)
        self.sq.register(self.qv_humi)
        self.sq.register(self.qv_pressure)
        self.sq.register(self.qv_airquality)

    def update (self, rrd):
        ### TODO validate data
        items = rrd.split(":")
        self.qv_temp.value = f"{float(items[1]):.1f}"
        self.qv_humi.value = f"{float(items[2]):.1f}"
        self.qv_pressure.value = f"{float(items[3]):.1f}"
        self.qv_airquality.value = f"{float(items[4]):.1f}"


###############################################################################
# Weather_Kollerberg ##########################################################
class Weather_Kollerberg (object):
    def __init__ (self):
        self.qv_kb_i_t = SensorValue("ID_21", "Temp KB indoor", SensorValue_Data.Types.Temp, "°C")
        self.qv_kb_i_h = SensorValue("ID_22", "Humi KB indoor", SensorValue_Data.Types.Humi, "% rF")
        self.qv_kb_p   = SensorValue("ID_23", "Pressure KB",    SensorValue_Data.Types.Pressure, "hPa")

        self.qv_kb_a_t = SensorValue("ID_24", "Temp KB outdoor", SensorValue_Data.Types.Temp, "°C")
        self.qv_kb_a_h = SensorValue("ID_25", "Humi KB outdoor", SensorValue_Data.Types.Humi, "% rF")

        self.qv_kb_k_t = SensorValue("ID_26", "Temp KB basement", SensorValue_Data.Types.Temp, "°C")
        self.qv_kb_k_h = SensorValue("ID_27", "Humi KB basement", SensorValue_Data.Types.Humi, "% rF")

        self.sq = SQ()
        self.sq.register(self.qv_kb_i_t)
        self.sq.register(self.qv_kb_i_h)
        self.sq.register(self.qv_kb_p)
        self.sq.register(self.qv_kb_a_t)
        self.sq.register(self.qv_kb_a_h)
        self.sq.register(self.qv_kb_k_t)
        self.sq.register(self.qv_kb_k_h)

    def update (self, rrd):
        # example data in rrd: pik-a,N:14.50:14.93:34.70:-7.51:1013.25:0.00
        (source, values) = rrd.split(',')
        if source == "pik-i":                 ### TODO: use f-notation
            self.qv_kb_i_t.value = "{:.1f}".format(float(values.split(':')[1]))
            self.qv_kb_i_h.value = "{:.1f}".format(float(values.split(':')[4]))
            self.qv_kb_p.value   = "{:.1f}".format(float(values.split(':')[5]))
        if source == "pik-a":
            self.qv_kb_a_t.value = "{:.1f}".format(float(values.split(':')[1]))
            self.qv_kb_a_h.value = "{:.1f}".format(float(values.split(':')[4]))
        if source == "pik-k":
            self.qv_kb_k_t.value = "{:.1f}".format(float(values.split(':')[1]))
            self.qv_kb_k_h.value = "{:.1f}".format(float(values.split(':')[4]))


###############################################################################
# Homeautomation ##############################################################
class Homeautomation (object):
    def __init__ (self):
        self.qv_temp       = SensorValue("ID_40", "TempKueche", SensorValue_Data.Types.Temp, "°C")
        self.qv_humi       = SensorValue("ID_41", "HumiKueche", SensorValue_Data.Types.Humi, "% rF")
        self.qv_pressure   = SensorValue("ID_42", "PressureKueche", SensorValue_Data.Types.Pressure, "hPa")
        self.qv_light      = SensorValue("ID_43", "LightKueche", SensorValue_Data.Types.Light, "lux")
        self.qv_airquality = SensorValue("ID_44", "AirQualityKueche", SensorValue_Data.Types.AirQuality, "%")

        self.sq = SQ()
        self.sq.register(self.qv_temp)
        self.sq.register(self.qv_humi)
        self.sq.register(self.qv_pressure)
        self.sq.register(self.qv_light)
        self.sq.register(self.qv_airquality)

    def update (self, rrd):
        ### TODO validate data
        items = rrd.split(":")
        self.qv_temp.value = f"{float(items[1]):.1f}"
        self.qv_humi.value = f"{float(items[3]):.1f}"
        self.qv_pressure.value = f"{float(items[4]):.1f}"
        self.qv_light.value = f"{float(items[5]):.1f}"
        self.qv_airquality.value = f"{float(items[6]):.1f}"


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
    weather_outdoor = Weather_Outdoor()
    weather_indoor = Weather_Indoor()
    weather_kollerberg = Weather_Kollerberg()
    homeautomation = Homeautomation()

    r = Receiver()
    r.start()

# eof #

