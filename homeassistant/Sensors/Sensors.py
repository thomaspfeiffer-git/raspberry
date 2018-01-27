#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
##############################################################################
# Sensors.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git 2018                             #
##############################################################################
"""
"""

### usage ###
# run programm: nohup ./Sensors.py &

import sys
import time

sys.path.append('../../libs')
sys.path.append('../../libs/sensors')

from i2c import I2C
from Measurements import Measurements
from sensors.BME680 import BME680, BME_680_SECONDARYADDR
from sensors.TSL2561 import TSL2561
from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data
from Shutdown import Shutdown



###############################################################################
# shutdown_application ########################################################
def shutdown_application ():
    """called on shutdown; stops all threads"""
    print("in shutdown_application()")
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    bme680  = BME680(i2c_addr=BME_680_SECONDARYADDR)
    tsl2561 = TSL2561()

    while True:
        bme680.get_sensor_data()
        print("{:.2f} °C; {:.2f} hPa; {:.2f} % rF; air quality: {}".format(bme680.data.temperature, bme680.data.pressure, bme680.data.humidity, bme680.data.air_quality_score))
        print("{:.2f} lux".format(tsl2561.lux()))
        time.sleep(10)

    

# eof #

