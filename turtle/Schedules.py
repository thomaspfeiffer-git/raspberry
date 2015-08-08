###############################################################################################
# Schedules.py                                                                                #
# Schedule data for heating and light                                                         #
# (c) https://github.com/thomaspfeiffer-git 2015                                              #
###############################################################################################

import datetime
from time import *


class heat:
   schedule = [[5 for m in range(60)] for h in range(24)]

   schedule[ 7][0:59] = [25 for m in range(60)]
   schedule[ 8][0:59] = [25 for m in range(60)]
   schedule[ 9][0:59] = [25 for m in range(60)]
   schedule[10][0:59] = [30 for m in range(60)]
   schedule[11][0:59] = [30 for m in range(60)]
   schedule[12][0:59] = [30 for m in range(60)]
   schedule[13][0:59] = [25 for m in range(60)]
   schedule[14][0:59] = [25 for m in range(60)]
   schedule[15][0:59] = [20 for m in range(60)]
   schedule[16][0:29] = [18 for m in range(30)]
 


class light:
   schedule = [[[5 for m in range(60)] for h in range(24)] for M in range(53)]

   schedule[32][ 8][0:59] = [35 for m in range(60)]
   schedule[32][ 9][0:59] = [35 for m in range(60)]
   schedule[32][10][0:59] = [35 for m in range(60)]
   schedule[32][11][0:59] = [35 for m in range(60)]
   schedule[32][12][0:59] = [35 for m in range(60)]
   schedule[32][13][0:59] = [35 for m in range(60)]

   schedule[33][ 8][0:59] = [35 for m in range(60)]
   schedule[33][ 9][0:59] = [35 for m in range(60)]
   schedule[33][10][0:59] = [35 for m in range(60)]
   schedule[33][11][0:59] = [35 for m in range(60)]
   schedule[33][12][0:59] = [35 for m in range(60)]
   schedule[33][13][0:59] = [35 for m in range(60)]

   schedule[34][ 8][0:59] = [35 for m in range(60)]
   schedule[34][ 9][0:59] = [35 for m in range(60)]
   schedule[34][10][0:59] = [35 for m in range(60)]
   schedule[34][11][0:59] = [35 for m in range(60)]
   schedule[34][12][0:59] = [35 for m in range(60)]
   schedule[34][13][0:59] = [35 for m in range(60)]



### eof ###
