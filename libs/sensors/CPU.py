# -*- coding: utf-8 -*-
##############################################################################
# CPU.py                                                                     #
# Encapsulates CPU temp stuff                                                #
# (c) https://github.com/thomaspfeiffer-git 2015, 2016                       #
##############################################################################
"""encapsulates CPU temp stuff"""

import subprocess
import sys

sys.path.append('../libs/sensors/Adafruit')
from Adafruit import Adafruit_GPIO_Platform as Platform


class CPU:
    def __init__(self):
        pass


    def __raspberryPi (self):
        res = subprocess.check_output(["vcgencmd", "measure_temp"])
        return float(res.replace("temp=","").replace("'C\n",""))


    def __nanoPi (self):
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            return float(f.read())

    def read_temperature (self):
        plat = Platform.platform_detect()
        if plat == Platform.RASPBERRY_PI:
            return self.__raspberryPi()
        elif plat == Platform.NANOPI:
            return self.__nanoPi()
        else:
            return None

### eof ###

