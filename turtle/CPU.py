##############################################################################
# CPU.py                                                                     #
# Encapsulates CPU temp stuff                                                #
# (c) https://github.com/thomaspfeiffer-git 2015                             #
##############################################################################
"""encapsulates CPU temp stuff"""

import os

class CPU:
    def __init__(self):
        pass

    def read(self):
        res = os.popen('vcgencmd measure_temp').readline()
        return(float(res.replace("temp=","").replace("'C\n","")))

### eof ###

