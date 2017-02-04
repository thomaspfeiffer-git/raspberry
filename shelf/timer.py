# -*- coding: utf-8 -*-
############################################################################
# timer.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""implements a threaded scheduler"""

import sched
from time import sleep, time
import threading

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
            print("Cancel")
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

