# -*- coding: utf-8 -*-
##############################################################################
# CPU.py                                                                     #
# Encapsulates CPU temp stuff                                                #
# (c) https://github.com/thomaspfeiffer-git 2015                             #
##############################################################################
"""encapsulates CPU temp stuff"""

import subprocess

class CPU:
    def __init__(self):
        pass

    def read(self):
        res = subprocess.check_output(["vcgencmd", "measure_temp"])
        return float(res.replace("temp=","").replace("'C\n",""))

### eof ###

