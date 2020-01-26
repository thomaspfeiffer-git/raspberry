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

import sys
sys.path.append("../libs/")

from Config import CONFIG
from Logging import Log


###############################################################################
# State #######################################################################
class State (object):
    class States (Enum):
        on = 1
        off = 0

    def __init__ (self, min_on_time, min_off_time):
        self.min_on_time = datetime.timedelta(seconds=min_on_time)
        self.min_off_time = datetime.timedelta(seconds=min_off_time)
        self.last_on = datetime.datetime(year=1970, month=1, day=1)
        self.last_off = datetime.datetime(year=1970, month=1, day=1)
        self.__state = State.States.off

    @property
    def state (self):
        return self.__state

    @state.setter
    def state (self, newstate):
        now = datetime.datetime.now()
        if self.state == State.States.off and newstate == State.States.on:
            if self.last_off + self.min_off_time < now:
                self.__state = State.States.on
                self.last_on = now
        elif self.state == State.States.on and newstate == State.States.off:
            if self.last_on + self.min_on_time < now:
                self.__state = State.States.off
                self.last_off = now


###############################################################################
# Schedule ####################################################################
class Schedule (object):
    all_conditions = ['time', 'temperature', 'humidity_difference', 'humidity']

    def __init__ (self):
        self.schedule = None
        with open(CONFIG.Schedule.file) as fd:
            xmldoc = xmltodict.parse(fd.read())

        xmldoc['valid_until'] = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0)
        xmldoc['min_on_time'] = int(xmldoc['schedules']['min_on_time']) * 60
        xmldoc['min_off_time'] = int(xmldoc['schedules']['min_off_time']) * 60
        xmldoc['schedules'].pop('min_on_time', None)
        xmldoc['schedules'].pop('min_off_time', None)

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


    def validate_humidity (self, condition):
        direction = condition['@direction']
        if direction not in ['in', 'out']:
            raise ValueError(f"'@direction' is '{direction}', should be in ['in', 'out']")

        value = float(condition['value'])
        if not 0 <= value <= 100:
            raise ValueError(f"'value is '{value}', should be in 0 .. 100")
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


###############################################################################
# Scheduler ###################################################################
class Scheduler (threading.Thread):
    all_checks = ['time', 'temperature', 'humidity', 'humidity_difference']

    def __init__ (self, sensordata):
        threading.Thread.__init__(self)
        self.sensordata = sensordata
        self.__lock = threading.Lock()
        self.load_schedule()
        self.state = State(self.schedule.schedule['min_on_time'], self.schedule.schedule['min_off_time'])
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
        if not self.sensordata.valid:
            return False

        if condition['@location'] == 'outside':
            measurement = self.sensordata.outdoor_temp
        else:
            raise NotImplementedError("Other locations than 'outside' not implemented yet.")

        if condition['operator'](measurement, condition['value']):
            return True
        else:
            return False

    def check_humidity (self, condition):
        if not self.sensordata.valid:
            return False

        if datetime.datetime.now().minute in [0, 30]:
            return True

        if condition['@direction'] == 'in':
            measurement = self.sensordata.airin_humidity
        elif condition['@direction'] == 'out':
            measurement = self.sensordata.airout_humidity
        else:
            raise ValueError(f"'@direction' is '{direction}', should be in ['in', 'out']")

        if condition['operator'](measurement, condition['value']):
            return True
        else:
            return False

    def check_humidity_difference (self, condition):
        return True

    def check (self):
        if self.schedule.schedule['valid_until'] < datetime.datetime.now():
            self.load_schedule()

        with self.__lock:
            on = False
            for schedule in self.schedule.schedule['schedules']['schedule']:
                on = self.check_time(schedule)

                if 'conditions' in schedule:
                    for check in schedule['conditions']:
                        if not check in Scheduler.all_checks:
                            raise NameError(f"Check '{check}' not defined.")
                        fn = getattr(self, f"check_{check}")
                        on = on and fn(schedule['conditions'][check])

                if on:
                    break

            self.state.state = State.States.on if on else State.States.off

    def run (self):
        while self._running:
            self.check()

            for _ in range(500):      # interruptible sleep
                if not self._running:
                    break
                time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
## main #######################################################################
""" for testing purposes only """
if __name__ == "__main__":
    from Sensors import Sensordata
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    data = Sensordata()
    data.airin_humidity = 95.0
    data.airout_humidity = 99.0
    data.valid = True
    s = Scheduler(data)
    s.check()
    # pp.pprint(s.schedule.schedule)

    sys.exit(0)
    i = 0
    while i < 2000:
        time.sleep(60)
        s.check()
        i += 1


# eof #

