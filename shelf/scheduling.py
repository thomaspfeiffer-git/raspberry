# -*- coding: utf-8 -*-
############################################################################
# scheduling.py                                                            #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""implements two classes for scheduling:
   - Time: provides just hour and minute
   - Timer: schedules an event (basically to switch of the LED strip
"""


from datetime import datetime
import sched
from time import sleep
import threading


############################################################################
# Time #####################################################################
class Time (object):
    def __init__ (self, hour=None, minute=None, string=None):
        if string:
            h, m = string.split(':')
            self.hour = int(h)
            self.minute = int(m)
        else:
            now = datetime.now()
            self.hour = int(hour) if hour else now.hour
            self.minute = int(minute) if minute else now.minute

    @property
    def hour (self):
        return self.__hour

    @hour.setter
    def hour (self, hour):
        if 0 <= hour <= 23:
            self.__hour = hour  
        else:
            raise ValueError("hour has to be in 0 .. 23")

    @property
    def minute (self):
        return self.__minute

    @minute.setter
    def minute (self, minute):
        if 0 <= minute <= 59:
            self.__minute = minute
        else:
            raise ValueError("minute has to be in 0 .. 59")

    def __str__ (self):
        return "{:d}:{:02d}".format(self.hour, self.minute)


############################################################################
# Timer ####################################################################
class Timer (threading.Thread):
    def __init__ (self, delayfunc):
        threading.Thread.__init__(self)
        self._event     = None
        self._scheduler = sched.scheduler()
        self._delayfunc = delayfunc
        self._running   = True
        self._setevent  = False
        
    def set (self, delay):
        self.cancel()
        self._delay = delay
        self._setevent = True

    def cancel (self):
        if self._event:
            self._scheduler.cancel(self._event)

    def run (self):
        while self._running:
            sleep(0.01)
            if self._setevent:
                self._setevent = False
                self._event = self._scheduler.enter(self._delay, 1, self._delayfunc)
                self._scheduler.run()
                self._event = None # clear _event after event has expired

    def stop (self):
        self._running = False
        self.cancel()

# eof #

