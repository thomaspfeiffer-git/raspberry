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
    def __init__ (self):
        self.fan_in = Fan(65)
        self.fan_out = Fan(66)
        self.fan_box = Fan(67)

    def ventilation_on (self):
        pass
        # foreach fan: on

    def ventilation_off (self):
        pass
        # foreach fan: off

    def run (self):
        pass

    def stop (self):
        self.fan_in.close()   # TODO: immediate close necessary on shutdown
        self.fan_out.close()
        self.fan_box.close()


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

#    display = Display(data)

#    udp_sender = UDP_Sender(data)
#    udp_sender.start()

#    sensors = Sensors(data,update_display=display.print)
#    sensors.start()

    control = Control()
    control.run()

# eof #

