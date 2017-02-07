# -*- coding: utf-8 -*-
############################################################################
# scheduling.py                                                            #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""implements classes for scheduling:
   - Time: provides a class with hour and minute only
   - Scheduling_Params: read params from request
   - Scheduling: tailor-made scheduler
"""

from datetime import datetime
import threading
import time


DEFAULT_ACTIVATE_TIME   = "--:--"   # = now()
DEFAULT_DEACTIVATE_TIME = "22:30"


############################################################################
# Time #####################################################################
class Time (object):
    """represents time with hours and minutes only"""
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
# Scheduling_Params ########################################################
class Scheduling_Params (object):
    def __init__ (self):
        self.reset()

    def reset (self):
        self.time_on   = None
        self.time_off  = None
        self.daily     = False
        self.permanent = False

    def get_scheduling_params (self, request_args):
        """reads parameters from request string:
           -on:    when to switch on the LEDs; default == now()
           -off:   when to switch off the LEDs; default == DEFAULT_DEACTIVATE_TIME
           -daily: daily schedule; default == False
           -permanent: always on; default == False
        """
        time_on   = request.args.get('on', DEFAULT_ACTIVATE_TIME)
        time_off  = request.args.get('off', DEFAULT_DEACTIVATE_TIME)
        daily     = request.args.get('daily', 'false')
        permanent = request.args.get('permanent', 'false')

        try:
            self.time_on   = Time() if time_on == DEFAULT_ACTIVATE_TIME else \
                             Time(string=time_on)
            self.time_off  = Time(string=time_off)
            self.daily     = False if daily == 'false' else True
            self.permanent = False if permanent == 'false' else True
        except ValueError:
            self.reset()
            return False
        else:
            return True

    def __str__ (self):
        retstr = "time on: {}; time off: {}; daily: {}; permanent: {}"
        return retstr.format(self.time_on, self.time_off, \
                             self.daily, self.permanent)


############################################################################
# Scheduling ###############################################################
class Scheduling (threading.Thread):
    """ tailor-made scheduler with dedicated functions for switching
        the LEDs on and off at specific times.
    """
    def __init__ (self, scheduling_params=None):
        threading.Thread.__init__(self)
        self._sp = scheduling_params if scheduling_params else Scheduling_Params()
        self._running = True

    def set_timings (self, scheduling_params):
        self._sp = scheduling_params

    def set_method_on (self, method, **kwargs):
        self._method_on = method
        self._kwargs_on = kwargs

    def set_method_off (self, method, **kwargs):
        self._method_off = method
        self._kwargs_off = kwargs

    def run (self):
        setting_on  = False  # call set_pattern() only once
        setting_off = False

        while self._running:
            now = datetime.now()
            if self._sp.permanent or self._sp.time_on:
                if self._sp.permanent or \
                   (now.hour   == self._sp.time_on.hour and \
                    now.minute == self._sp.time_on.minute):
                    if not setting_on:
                        self._method_on(**self._kwargs_on)
                        setting_on = True
                        # set time_on to None if event is scheduled only once.
                        if not self._sp.time_daily:
                            self._sp.time_on = None
                else:
                    setting_on = False
                                                # on has to be done before off
            if not self._sp.permanent and self._sp.time_off and \
               (not self._sp.time_on or self._sp.time_daily):
                if now.hour   == self._sp.time_off.hour and \
                   now.minute == self._sp.time_off.minute:
                    if not setting_off:
                        self._method_off(**self._kwargs_off)
                        setting_off = True
                        if not self._sp.time_daily:
                            self._sp.time_off = None
                else:
                    setting_off = False

            time.sleep(0.1)

    def stop (self):
        self._running = False

# eof #

