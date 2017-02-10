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
        self.lock = threading.Lock()
        self.reset()

    def reset (self):
        with self.lock:
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
        time_on   = request_args.get('on', DEFAULT_ACTIVATE_TIME)
        time_off  = request_args.get('off', DEFAULT_DEACTIVATE_TIME)
        daily     = request_args.get('daily', 'false')
        permanent = request_args.get('permanent', 'false')

        try:
            with self.lock:
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


    def set_pattern_method (self, pattern_method):
        self._pattern_method = pattern_method

    def set_timings (self, scheduling_params):
        self._sp = scheduling_params
        self.__is_on  = False
        self.__is_off = True

    """
    def set_method_on (self, setpattern_method, **kwargs):
        self._method_on = setpattern_method
        self._kwargs_on = kwargs

    def set_method_off (self, setpattern_method, **kwargs):
        self._method_off = setpattern_method # TODO: check: always c.set_pattern() ?
        self._kwargs_off = kwargs
    """

    def set_method_on (self, **kwargs):
        self._kwargs_on = kwargs

    def set_method_off (self, **kwargs):
        self._kwargs_off = kwargs

    def cancel (self):
        self._sp.reset()

    def run (self):
        self.__is_on  = False
        self.__is_off = True

        # TODO: now() < time_on < time_off (oder time_on/off => morgen?)
        while self._running:
            now = datetime.now()

            with self._sp.lock:
                if self._sp.permanent:
                    if not self.__is_on:  # avoid multiple calls to on()
                        # self._method_on(**self._kwargs_on)
                        self._pattern_method(**self._kwargs_on)
                        self.__is_on  = True
                        self.__is_off = False
                else:
                    if self._sp.time_on and \
                       now.hour   == self._sp.time_on.hour and \
                       now.minute == self._sp.time_on.minute:
                        if not self.__is_on: # avoid multiple calls to on()
                            # self._method_on(**self._kwargs_on)
                            self._pattern_method(**self._kwargs_on)
                            self.__is_on = True
                            self.__is_off = False
                            if not self._sp.daily:
                                self._sp.time_on = None

            with self._sp.lock:
                if not self._sp.permanent and self.__is_on:
                    if self._sp.time_off and \
                       now.hour   == self._sp.time_off.hour and \
                       now.minute == self._sp.time_off.minute:
                        if not self.__is_off: # avoid multiple calls to off()
                            # self._method_off(**self._kwargs_off)
                            self._pattern_method(**self._kwargs_off)
                            self.__is_off = True
                            self.__is_on  = False
                            if not self._sp.daily:
                                self._sp.time_off = None

            time.sleep(0.1)

    def stop (self):
        self._running = False

# eof #

