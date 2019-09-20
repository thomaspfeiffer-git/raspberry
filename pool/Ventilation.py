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
### TODO


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

    def __init__ (self):
        self.fans = {Control.fan_in: Fan(65, delay=10), 
                     Control.fan_out: Fan(66, delay=5), 
                     Control.fan_box: Fan(67, delay=0)}

    def ventilation_on (self):
        for f in self.fans.values():
            f.on()

    def ventilation_off (self):
        for f in self.fans.values():
            f.off()


    def set_optional (self, param):
        self.optional = param

    def run (self):
        schedule.every().day.at("14:00").do(self.ventilation_on)
        schedule.every().day.at("15:00").do(self.ventilation_off)


        schedule.every().day.at("07:00").do(self.set_optional, (True,))
        schedule.every().day.at("08:00").do(self.set_optional, (False,))
        while True:
            schedule.run_pending()
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
#    udp_sender.stop()
#    udp_sender.join()
#    sensors.stop()
#    sensors.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)
    data = Sensordata()

#    display = Display(data)

#    udp_sender = UDP_Sender(data)
#    udp_sender.start()

#    sensors = Sensors(data,update_display=display.print)
#    sensors.start()

    control = Control()
    control.run()

# eof #

