#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Ventilation.py                                                              #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                   #
###############################################################################

"""
Controls ventilation of the control room of our swimming pool.
"""

### Usage ###
# nohup ./Ventilation.py 2>&1 > ventilation.log &


### Packages you might need to install ###
# sudo pip3 install Pillow
# sudo pip3 install schedule


import schedule
import sys
import time


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown

from Display import Display
from Fan import Fan
from Sensors import Sensors, Sensordata
from UDP import UDP_Sender


###############################################################################
# Control #####################################################################
class Control (object):
    fan_in  = "fan_in"
    fan_out = "fan_out"
    fan_box = "fan_box"

    def __init__ (self, data):
        self.data = data
        self.run_optional = False
        self.fans = {Control.fan_in: Fan(65, delay=10), 
                     Control.fan_out: Fan(66, delay=5), 
                     Control.fan_box: Fan(67, delay=0)}

    def ventilation_on (self):
        self.data.fan1_on = 1  # TODO: Add per fan logic
        self.data.fan2_on = 1
        self.data.fan3_on = 1
        self.data.fan4_on = 1
        for f in self.fans.values():
            f.on()

    def ventilation_off (self):
        self.data.fan1_on = 0  # TODO: Add per fan logic
        self.data.fan2_on = 0
        self.data.fan3_on = 0
        self.data.fan4_on = 0
        for f in self.fans.values():
            f.off()

    def set_run_optional (self, param):
        self.run_optional = param

    def ventilation_optional (self):
        already_running = False

        def ventilation_optional_logic ():
            nonlocal already_running
            if self.run_optional and not already_running:
                # if humi_inside+5 > humi_outside:  # TODO: add some clever logic
                self.ventilation_on()
                already_running = True
            elif not self.run_optional and already_running:
                self.ventilation_off()
                already_running = False

        return ventilation_optional_logic        

    def run (self):
        ventilation_optional = self.ventilation_optional()

        schedule.every().day.at("10:00").do(self.ventilation_on)
        schedule.every().day.at("11:00").do(self.ventilation_off)
        schedule.every().day.at("12:38").do(self.ventilation_on)
        schedule.every().day.at("12:40").do(self.ventilation_off)
        schedule.every().day.at("13:00").do(self.ventilation_on)
        schedule.every().day.at("14:00").do(self.ventilation_off)
        schedule.every().day.at("15:46").do(self.ventilation_on)
        schedule.every().day.at("15:48").do(self.ventilation_off)
        schedule.every().day.at("16:00").do(self.ventilation_on)
        schedule.every().day.at("17:00").do(self.ventilation_off)
        schedule.every().day.at("17:15").do(self.ventilation_on)
        schedule.every().day.at("17:25").do(self.ventilation_off)
        schedule.every().day.at("19:00").do(self.ventilation_on)
        schedule.every().day.at("20:00").do(self.ventilation_off)
        schedule.every().day.at("22:00").do(self.ventilation_on)
        schedule.every().day.at("23:00").do(self.ventilation_off)

#        schedule.every().day.at("10:00").do(self.set_run_optional, True)
#        schedule.every().day.at("12:00").do(self.set_run_optional, False)

        while True:
            schedule.run_pending()
            ventilation_optional()
            time.sleep(1)

    def stop (self):
        for f in self.fans.values():
            f.close(immediate=True)


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    control.stop()
    udp_sender.stop()
    udp_sender.join()
    sensors.stop()
    sensors.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)
    data = Sensordata()

    display = Display(data)

    udp_sender = UDP_Sender(data)
    udp_sender.start()

    sensors = Sensors(data,update_display=display.print)
    sensors.start()

    control = Control(data)
    control.run()

# eof #

