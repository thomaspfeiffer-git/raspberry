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


import sys
import time



sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown

from Display import Display
from Sensors import Sensors, Sensordata
from UDP import UDP_Sender


# Fans (AirIn, AirOut):
# https://www.amazon.de/s?k=l%C3%BCfter+5v+60mm&__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss



###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
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

    while True:
        time.sleep(0.5)

# eof #

