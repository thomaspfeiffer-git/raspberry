# -*- coding: utf-8 -*-
############################################################################
# userinterface.py                                                         #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""implements classes for the user interface
"""

import copy
# import flask
from flask import Markup, render_template

from scheduling import Scheduling_Params


############################################################################
# Feedback - renders html template #########################################
class Feedback (object):
    """provides some basic functions for rendering the html template.
       basically error and success message are set in __init__().
       __str__() returns the rendered template including error and
       success message(s)
    """
    def __init__ (self, error="", success="", status=None):
        self.error   = error
        self.success = success
        self.status  = status

    def __str__ (self):
        return render_template('interface.html', \
                               error=self.error, success=self.success, \
                               status="{}".format(self.status))


############################################################################
# Status ###################################################################
class Status (object):
    def __init__ (self, brightness=0):
        self.brightness = brightness
        self.schedule = Scheduling_Params()
        self.reset()

    def reset (self):
        """resets dependant parameters
           eg 'pattern' has no color, 'color' has no delay"""
        self.pattern = ""
        self.delay   = ""
        self.color   = ""

    def set (self, **kwargs):
        """sets dependant parameters"""
        self.reset()
        for key, value in kwargs.items():
            self.__dict__[key] = value
       
    @property
    def brightness (self):
        return self.__brightness

    @brightness.setter
    def brightness (self, value):
        self.__brightness = value 

    @property
    def schedule (self):
        return self.__schedule

    @schedule.setter
    def schedule (self, schedule):
        self.__schedule = copy.copy(schedule)

    def loginfo (self):
        return "pattern: {0.pattern}; delay: {0.delay}; color: {0.color}; brightness: {0.brightness}; time on: {1.time_on}; time off: {1.time_off}; daily: {1.daily}; permanent: {1.permanent}".format(self, self.schedule)

    def __str__ (self):
        ret = "<tr><td>pattern:    </td><td>{}</td></tr>\n".format(self.pattern) + \
              "<tr><td>delay:      </td><td>{}</td></tr>\n".format(self.delay) + \
              "<tr><td>color:      </td><td>{}</td></tr>\n".format(self.color) + \
              "<tr><td>brightness: </td><td>{}</td></tr>\n".format(self.brightness) + \
              "<tr><td>time on:    </td><td>{}</td></tr>\n".format(self.schedule.time_on) + \
              "<tr><td>time off:   </td><td>{}</td></tr>\n".format(self.schedule.time_off) + \
              "<tr><td>daily:      </td><td>{}</td></tr>\n".format(self.schedule.daily) + \
              "<tr><td>permanent:  </td><td>{}</td></tr>\n".format(self.schedule.permanent)
        return Markup(ret)

# eof #

