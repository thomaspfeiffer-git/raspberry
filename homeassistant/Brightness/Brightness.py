#!/usr/bin/python3
# -*- coding: utf-8 -*-
##############################################################################
# Brightness.py                                                              #
# (c) https://github.com/thomaspfeiffer-git 2017                             #
##############################################################################
"""controls brightness of a raspberry pi display based on the
   luminosity measured by a TSL2561"""


### usage ###
# TODO 


# Adjusting lightness
# cd /sys/class/backlight/rpi_backlight/
# sudo bash -c 'echo "255" > brightness'
# def _set_value(name, value):
#    with open(os.path.join(PATH, name), "w") as f:
#        f.write(str(value))
#


import subprocess
import sys
import time

sys.path.append('../../libs')
sys.path.append('../../libs/sensors')  # TODO beautify import paths
sys.path.append('../../libs/sensors/Adafruit')

from i2c import I2C
from sensors.TSL2561 import TSL2561

sensor = TSL2561()



while True:
    lux = int(sensor.lux()) * 2
    if lux < 15: lux = 15
    if lux > 255: lux = 255
    # TODO: call only on change of value etc
    # command = "./brightness {}".format(lux)
    command = "sudo bash -c \"echo \\\"{}\\\" > /sys/class/backlight/rpi_backlight/brightness\"".format(lux)

    # print("command:", command)
    subprocess.call(command, shell=True)

    time.sleep(1)

# eof #

