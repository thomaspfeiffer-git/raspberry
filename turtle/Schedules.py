##############################################################################
# Schedules.py                                                               #
# Schedule data for heating and light                                        #
# (c) https://github.com/thomaspfeiffer-git 2015                             #
##############################################################################

import datetime
from time import localtime


class ScheduleBase (object):
    def ts(self):
        hh, mm = localtime()[3:5]
        dy     = datetime.datetime.utcnow().isocalendar()[1]
        # print "Calender week:", dy
        return [dy, hh, mm]


class ScheduleHeat (ScheduleBase):
    __schedule = [[5 for m in range(60)] for h in range(24)]

    __schedule[ 7][0:59] = [28 for m in range(60)]
    __schedule[ 8][0:59] = [28 for m in range(60)]
    __schedule[ 9][0:59] = [28 for m in range(60)]
    __schedule[10][0:59] = [32 for m in range(60)]
    __schedule[11][0:59] = [32 for m in range(60)]
    __schedule[12][0:59] = [32 for m in range(60)]
    __schedule[13][0:59] = [25 for m in range(60)]
    __schedule[14][0:59] = [25 for m in range(60)]
    __schedule[15][0:59] = [20 for m in range(60)]
    __schedule[16][0:29] = [18 for m in range(30)]
 

    def on (self, value):
        dy, hh, mm = self.ts()
        if (self.__schedule[hh][mm] > value):
            return True
        else:
            return False 


class ScheduleLight (ScheduleBase):
    __schedule = [[[5 for m in range(60)] for h in range(24)] for w in range(53)]

    __tmax = 40
    __schedule[32][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[32][10][0:59] = [__tmax for m in range(60)]
    __schedule[32][11][0:59] = [__tmax for m in range(60)]
    __schedule[32][12][0:59] = [__tmax for m in range(60)]
    __schedule[32][13][0:59] = [__tmax for m in range(60)]

    __schedule[33][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[33][10][0:59] = [__tmax for m in range(60)]
    __schedule[33][11][0:59] = [__tmax for m in range(60)]
    __schedule[33][12][0:59] = [__tmax for m in range(60)]
    __schedule[33][13][0:59] = [__tmax for m in range(60)]
 
    __schedule[34][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[34][10][0:59] = [__tmax for m in range(60)]
    __schedule[34][11][0:59] = [__tmax for m in range(60)]
    __schedule[34][12][0:59] = [__tmax for m in range(60)]
    __schedule[34][13][0:59] = [__tmax for m in range(60)]

    __schedule[35][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[35][10][0:59] = [__tmax for m in range(60)]
    __schedule[35][11][0:59] = [__tmax for m in range(60)]
    __schedule[35][12][0:59] = [__tmax for m in range(60)]
    __schedule[35][13][0:59] = [__tmax for m in range(60)]


    def on (self, value):
        dy, hh, mm = self.ts()
        if (self.__schedule[dy][hh][mm] > value):
            return True
        else:
            return False 


class Control (object):
    def __init__(self, schedule, lamp):
        self.__schedule = schedule
        self.__lamp     = lamp


    def control (self, value):
        if (self.__schedule.on(value)): 
            self.__lamp.on()
        else:
            self.__lamp.off() 

### eof ###

