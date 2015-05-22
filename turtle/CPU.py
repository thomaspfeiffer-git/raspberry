###############################################################################################
# CPU.py                                                                                      #
# Encapsulates CPU temp stuff                                                                 #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################

import os

class CPU:
   def read(self):
      res = os.popen('vcgencmd measure_temp').readline()
      return(float(res.replace("temp=","").replace("'C\n","")))

### eof ###

