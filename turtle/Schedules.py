##############################################################################
# Schedules.py                                                               #
# Schedule data for heating and light                                        #
# (c) https://github.com/thomaspfeiffer-git 2015                             #
##############################################################################
"""schedule data for heating and light"""

import datetime
from time import localtime


class ScheduleBase (object):
    """base for schedule classes. provides a timestamp method"""
    def timestamp(self):
        hour, minute = localtime()[3:5]
        week         = datetime.datetime.utcnow().isocalendar()[1]
        # print "Calender week:", week_of_year
        return [week, hour, minute]


class ScheduleHeat (ScheduleBase):
    """schedule class for heating"""
    __schedule = [[7.0 for m in range(60)] for h in range(24)]

#    __schedule[11][30:59] = [32 for m in range(30)]
#    __schedule[12][0:59] = [32 for m in range(60)]
#    __schedule[13][0:29] = [30 for m in range(30)]
 

    def on (self, value):
        week, hour, minute = self.timestamp()

        if (hour > 2) and (hour < 22):     # some kind of very strange daylight saving
            hour += 1

        if (self.__schedule[hour][minute] > value):
            return True
        else:
            return False 


class ScheduleLight (ScheduleBase):
    """schedule class for lighting"""
    __schedule = [[[5 for m in range(60)] for h in range(24)] for w in range(53)]

    __tmax = 40
    __schedule[32][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[32][10][0:59] = [__tmax for m in range(60)]
    __schedule[32][11][0:59] = [__tmax for m in range(60)]
    __schedule[32][12][0:59] = [__tmax for m in range(60)]
    __schedule[32][13][0:59] = [__tmax for m in range(60)]
    __schedule[32][14][0:59] = [__tmax for m in range(60)]
    __schedule[32][15][0:59] = [__tmax for m in range(60)]

    __schedule[33][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[33][10][0:59] = [__tmax for m in range(60)]
    __schedule[33][11][0:59] = [__tmax for m in range(60)]
    __schedule[33][12][0:59] = [__tmax for m in range(60)]
    __schedule[33][13][0:59] = [__tmax for m in range(60)]
    __schedule[33][14][0:59] = [__tmax for m in range(60)]
    __schedule[33][15][0:59] = [__tmax for m in range(60)]
 
    __schedule[34][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[34][10][0:59] = [__tmax for m in range(60)]
    __schedule[34][11][0:59] = [__tmax for m in range(60)]
    __schedule[34][12][0:59] = [__tmax for m in range(60)]
    __schedule[34][13][0:59] = [__tmax for m in range(60)]
    __schedule[34][14][0:59] = [__tmax for m in range(60)]
    __schedule[34][15][0:59] = [__tmax for m in range(60)]

    __schedule[35][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[35][10][0:59] = [__tmax for m in range(60)]
    __schedule[35][11][0:59] = [__tmax for m in range(60)]
    __schedule[35][12][0:59] = [__tmax for m in range(60)]
    __schedule[35][13][0:59] = [__tmax for m in range(60)]
    __schedule[35][14][0:59] = [__tmax for m in range(60)]
    __schedule[35][15][0:59] = [__tmax for m in range(60)]

    __schedule[36][ 8][0:59] = [__tmax for m in range(60)]
    __schedule[36][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[36][10][0:59] = [__tmax for m in range(60)]
    __schedule[36][11][0:59] = [__tmax for m in range(60)]
    __schedule[36][12][0:59] = [__tmax for m in range(60)]
    __schedule[36][13][0:59] = [__tmax for m in range(60)]
    __schedule[36][14][0:59] = [__tmax for m in range(60)]
    __schedule[36][15][0:59] = [__tmax for m in range(60)]

    __schedule[37][ 8][0:59] = [__tmax for m in range(60)]
    __schedule[37][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[37][10][0:59] = [__tmax for m in range(60)]
    __schedule[37][11][0:59] = [__tmax for m in range(60)]
    __schedule[37][12][0:59] = [__tmax for m in range(60)]
    __schedule[37][13][0:59] = [__tmax for m in range(60)]
    __schedule[37][14][0:59] = [__tmax for m in range(60)]
    __schedule[37][15][0:59] = [__tmax for m in range(60)]

    __schedule[38][ 8][0:59] = [__tmax for m in range(60)]
    __schedule[38][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[38][10][0:59] = [__tmax for m in range(60)]
    __schedule[38][11][0:59] = [__tmax for m in range(60)]
    __schedule[38][12][0:59] = [__tmax for m in range(60)]
    __schedule[38][13][0:59] = [__tmax for m in range(60)]
    __schedule[38][14][0:59] = [__tmax for m in range(60)]
    __schedule[38][15][0:59] = [__tmax for m in range(60)]

    __schedule[39][ 8][0:59] = [__tmax for m in range(60)]
    __schedule[39][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[39][10][0:59] = [__tmax for m in range(60)]
    __schedule[39][11][0:59] = [__tmax for m in range(60)]
    __schedule[39][12][0:59] = [__tmax for m in range(60)]
    __schedule[39][13][0:59] = [__tmax for m in range(60)]
    __schedule[39][14][0:59] = [__tmax for m in range(60)]
    __schedule[39][15][0:59] = [__tmax for m in range(60)]

    __schedule[40][ 8][0:59] = [__tmax for m in range(60)]
    __schedule[40][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[40][10][0:59] = [__tmax for m in range(60)]
    __schedule[40][11][0:59] = [__tmax for m in range(60)]
    __schedule[40][12][0:59] = [__tmax for m in range(60)]
    __schedule[40][13][0:59] = [__tmax for m in range(60)]
    __schedule[40][14][0:59] = [__tmax for m in range(60)]

    __schedule[41][ 8][0:59] = [__tmax for m in range(60)]
    __schedule[41][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[41][10][0:59] = [__tmax for m in range(60)]
    __schedule[41][11][0:59] = [__tmax for m in range(60)]
    __schedule[41][12][0:59] = [__tmax for m in range(60)]
    __schedule[41][13][0:59] = [__tmax for m in range(60)]
    __schedule[41][14][0:59] = [__tmax for m in range(60)]

    __schedule[42][ 9][0:59] = [__tmax for m in range(60)]
    __schedule[42][10][0:59] = [__tmax for m in range(60)]
    __schedule[42][11][0:59] = [__tmax for m in range(60)]
    __schedule[42][12][0:59] = [__tmax for m in range(60)]
    __schedule[42][13][0:59] = [__tmax for m in range(60)]
    __schedule[42][14][0:59] = [__tmax for m in range(60)]

    __schedule[43][ 9][30:59] = [__tmax for m in range(30)]
    __schedule[43][10][0:59] = [__tmax for m in range(60)]
    __schedule[43][11][0:59] = [__tmax for m in range(60)]
    __schedule[43][12][0:59] = [__tmax for m in range(60)]
    __schedule[43][13][0:59] = [__tmax for m in range(60)]
    __schedule[43][14][0:59] = [__tmax for m in range(60)]

    __schedule[44][10][0:59] = [__tmax for m in range(60)] # End of daylight saving time.
    __schedule[44][11][0:59] = [__tmax for m in range(60)]
    __schedule[44][12][0:59] = [__tmax for m in range(60)]
    __schedule[44][13][0:59] = [__tmax for m in range(60)]
    __schedule[44][14][0:29] = [__tmax for m in range(30)]

    __schedule[45][10][30:59] = [__tmax for m in range(30)]
    __schedule[45][11][0:59] = [__tmax for m in range(60)]
    __schedule[45][12][0:59] = [__tmax for m in range(60)]
    __schedule[45][13][0:59] = [__tmax for m in range(60)]
    __schedule[45][14][0:29] = [__tmax for m in range(30)]

    __schedule[46][11][0:59] = [__tmax for m in range(60)]
    __schedule[46][12][0:59] = [__tmax for m in range(60)]
    __schedule[46][13][0:59] = [__tmax for m in range(60)]
    __schedule[46][14][0:29] = [__tmax for m in range(30)]

#    __schedule[47][11][30:59] = [__tmax for m in range(30)]
#    __schedule[47][12][0:59] = [__tmax for m in range(60)]
#    __schedule[47][13][0:59] = [__tmax for m in range(60)]
#    __schedule[47][14][0:29] = [__tmax for m in range(30)]

    def on (self, value):
        week, hour, minute = self.timestamp()

        if (hour > 2) and (hour < 22):     # some kind of very strange daylight saving
            hour += 1

        if (self.__schedule[week][hour][minute] > value):
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

