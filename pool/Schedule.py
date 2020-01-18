#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Schedule.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2020                   #
###############################################################################

"""
Implements the scheduler.
"""

import datetime
from enum import Enum
import operator
import threading
import time
import xmltodict

from Config import CONFIG
from Logging import Log


###############################################################################
# State #######################################################################
class State (object):
    class States (Enum):
        on = 1
        off = 0

    def __init__ (self, min_on_time, min_off_time):
        self.min_on_time = datetime.timedelta(seconds=min_on_time*60)
        self.min_off_time = datetime.timedelta(seconds=min_off_time*60)
        self.last_on = datetime.datetime(year=1970, month=1, day=1)
        self.last_off = datetime.datetime(year=1970, month=1, day=1)
        self.__state = State.States.off

    @property
    def state (self):
        return self.__state

    @state.setter
    def state (self, newstate):
        if self.state == State.States.off and newstate == State.States.on:
            if self.last_off + self.min_off_time < datetime.datetime.now():
                self.__state = State.States.on
                self.last_on = datetime.datetime.now()
        elif self.state == State.States.on and newstate == State.States.off:
            if self.last_on + self.min_on_time < datetime.datetime.now():
                self.__state = State.States.off
                self.last_off = datetime.datetime.now()


###############################################################################
# Schedule ####################################################################
class Schedule (object):
    all_conditions = ['time', 'temperature', 'humidity_difference']

    def __init__ (self):
        self.schedule = None
        with open(CONFIG.Schedule.file) as fd:
            xmldoc = xmltodict.parse(fd.read())

        xmldoc['valid_until'] = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0)
        xmldoc['min_on_time'] = CONFIG.Schedule.min_on_time
        xmldoc['min_off_time'] = CONFIG.Schedule.min_off_time

        for schedule in xmldoc['schedules']['schedule']:
            self.validate_time(schedule)

            if 'conditions' in schedule:
                for condition in schedule['conditions']:
                    if not condition in Schedule.all_conditions:
                        raise NameError(f"Condition '{condition}' not defined.")
                    fn = getattr(self, f"validate_{condition}")
                    fn(schedule['conditions'][condition])

        self.schedule = xmldoc

    def validate_time (self, schedule):
        def validate (t):
            try:
                t = datetime.datetime.strptime(t, "%H:%M")
            except ValueError:
                raise ValueError(f"'start' is '{t}', should be '%H:%M'")
            return lambda: datetime.datetime.now().replace(hour=t.hour, minute=t.minute)

        schedule['start'] = validate(schedule['start'])
        schedule['stop'] = validate(schedule['stop'])

        if schedule['stop']() < schedule['start']():
            raise ValueError(f"starttime '{schedule['start']()}' is after " +
                             f"stoptime '{schedule['stop']()}'")


    def validate_temperature (self, condition):
        location = condition['@location']
        if location not in ['inside', 'outside']:
            raise ValueError(f"'@location' is '{location}', should be in ['inside', 'outside']")

        value = float(condition['value'])
        if not -10 <= value <= 50:
            raise ValueError(f"'value is '{value}', should be in -10 .. +50")
        condition['value'] = value

        operator_ = condition['operator']
        if operator_ not in ['<=', '>=']:
            raise ValueError(f"'operator' is '{operator_}', should be in ['<=', '>=']")
        condition['operator'] = {'>=': operator.ge, '<=': operator.le}[operator_]


    def validate_humidity_difference (self, condition):
        value = float(condition['value'])
        if not 1 <= value <= 50:
            raise ValueError(f"'value is '{value}', should be in 1 .. +50")
        condition['value'] = value

        delay_for_measurement = int(condition['delay_for_measurement'])
        if delay_for_measurement < 1:
            raise ValueError(f"'delay_for_measurement' is '{delay_for_measurement}', should be >= 1")
        condition['delay_for_measurement'] = delay_for_measurement

        delay_for_retry = int(condition['delay_for_retry'])
        if delay_for_retry < 1:
            raise ValueError(f"'delay_for_retry' is '{delay_for_retry}', should be >= 1")
        condition['delay_for_retry'] = delay_for_retry


###############################################################################
# Scheduler ###################################################################
class Scheduler (threading.Thread):
    def __init__ (self, sensordata):
        threading.Thread.__init__(self)
        self.sensordata = sensordata
        self.__lock = threading.Lock()
        self.state = State(CONFIG.Schedule.min_on_time, CONFIG.Schedule.min_off_time)
        self.load_schedule()
        self._running = True

    def load_schedule (self):
        with self.__lock:
            self.schedule = Schedule()
            Log("Schedule loaded.")

    def check_time (self, condition):
        if condition['start']() <= datetime.datetime.now() <= condition['stop']():
            return True
        else:
            return False

    def check_temperature (self, condition):
        pass

    def check (self):
        if self.schedule.schedule['valid_until'] < datetime.datetime.now():
            self.load_schedule()

        with self.__lock:
            on = False
            for schedule in self.schedule.schedule['schedules']['schedule']:
                on = self.check_time(schedule)

                if 'conditions' in schedule:
                   for condition in schedule['conditions']:
                       pass       # TODO

                if on:
                    break

            self.state.state = State.States.on if on else State.States.off

    def run (self):
        while self._running:
            self.check()

            for _ in range(600):      # interruptible sleep
                if not self._running:
                    break
                time.sleep(0.1)

    def stop (self):
        self._running = False

# eof #

