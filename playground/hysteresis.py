#!/usr/bin/python3 -u

import datetime
from enum import Enum
import sys
import time

sys.path.append("../libs/")
from Logging import Log

class Scheduler (object):
    class State (Enum):
        on = 1
        off = 0

    def __init__ (self, min_on_time, min_off_time):
        # self.min_on_time = datetime.timedelta(seconds=min_on_time*60)
        # self.min_off_time = datetime.timedelta(seconds=min_off_time*60)
        self.min_on_time = datetime.timedelta(seconds=min_on_time)
        self.min_off_time = datetime.timedelta(seconds=min_off_time)
        self.last_on = datetime.datetime(year=1970, month=1, day=1)
        self.last_off = datetime.datetime(year=1970, month=1, day=1)
        self.__state = Scheduler.State.off

    @property
    def state (self):
        return self.__state

    @state.setter
    def state (self, state_):
        if self.state == state_:
            Log(f"already in state '{state_}'")
        if self.state == Scheduler.State.off and state_ == Scheduler.State.on:
            if self.last_off + self.min_off_time < datetime.datetime.now():
                self.__state = Scheduler.State.on
                self.last_on = datetime.datetime.now()
                Log("on")
            else:
                Log("'on' not allowed currently.")
        elif self.state == Scheduler.State.on and state_ == Scheduler.State.off:
            if self.last_on + self.min_on_time < datetime.datetime.now():
                self.__state = Scheduler.State.off
                self.last_off = datetime.datetime.now()
                Log("off")
            else:
                Log("'off' not allowed currently.")


#########################
# main ##################

s = Scheduler(15,15)
s.state = Scheduler.State.on
time.sleep(10)
s.state = Scheduler.State.off
time.sleep(10)
s.state = Scheduler.State.on
time.sleep(1)
s.state = Scheduler.State.off
s.state = Scheduler.State.off
time.sleep(1)
Log("Ende")



