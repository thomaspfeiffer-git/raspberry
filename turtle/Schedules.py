###############################################################################################
# Schedules.py                                                                                #
# Schedule data for heating and light                                                         #
# (c) https://github.com/thomaspfeiffer-git 2015                                              #
###############################################################################################

import datetime
from time import *


class __schedule_base:
   def ts (self):
      hh, mm  = localtime()[3:5]
      dy      = datetime.datetime.utcnow().isocalendar()[1]
      return [dy,hh,mm]


class HeatControl (__schedule_base):
   __schedule = [[5 for m in range(60)] for h in range(24)]

   __schedule[ 7][0:59] = [25 for m in range(60)]
   __schedule[ 8][0:59] = [25 for m in range(60)]
   __schedule[ 9][0:59] = [25 for m in range(60)]
   __schedule[10][0:59] = [30 for m in range(60)]
   __schedule[11][0:59] = [30 for m in range(60)]
   __schedule[12][0:59] = [30 for m in range(60)]
   __schedule[13][0:59] = [25 for m in range(60)]
   __schedule[14][0:59] = [25 for m in range(60)]
   __schedule[15][0:59] = [20 for m in range(60)]
   __schedule[16][0:29] = [18 for m in range(30)]
 

   def __on (self,value):
      dy, hh, mm = self.ts()

      if (self.__schedule[hh][mm] > value):
         return True
      else:
         return False 


   def switch (self, lamp, value):
      if (self.__on(value)):
         lamp.on()
      else:
         lamp.off()



class LightControl (__schedule_base):
   __schedule = [[[5 for m in range(60)] for h in range(24)] for M in range(53)]

   __tmax = 40
   __schedule[32][ 8][0:59] = [__tmax for m in range(60)]
   __schedule[32][ 9][0:59] = [35 for m in range(60)]
   __schedule[32][10][0:59] = [35 for m in range(60)]
   __schedule[32][11][0:59] = [35 for m in range(60)]
   __schedule[32][12][0:59] = [35 for m in range(60)]
   __schedule[32][13][0:59] = [35 for m in range(60)]
   __schedule[32][20][0:59] = [35 for m in range(60)]

   __schedule[33][ 8][0:59] = [35 for m in range(60)]
   __schedule[33][ 9][0:59] = [35 for m in range(60)]
   __schedule[33][10][0:59] = [35 for m in range(60)]
   __schedule[33][11][0:59] = [35 for m in range(60)]
   __schedule[33][12][0:59] = [35 for m in range(60)]
   __schedule[33][13][0:59] = [35 for m in range(60)]

   __schedule[34][ 8][0:59] = [35 for m in range(60)]
   __schedule[34][ 9][0:59] = [35 for m in range(60)]
   __schedule[34][10][0:59] = [35 for m in range(60)]
   __schedule[34][11][0:59] = [35 for m in range(60)]
   __schedule[34][12][0:59] = [35 for m in range(60)]
   __schedule[34][13][0:59] = [35 for m in range(60)]


   def __on (self, value):
      dy, hh, mm = self.ts()

      if (self.__schedule[dy][hh][mm] > value):
         return True
      else:
         return False 


   def switch (self, lamp, value):
      if (self.__on(value)):
         lamp.on()
      else:
         lamp.off()


### eof ###

