# -*- coding: utf-8 -*-
################################################################################
# SensorValue.py                                                               #
# Class providing various data of sensors                                      #
# (c) https://github.com/thomaspfeiffer-git 2016                               #
################################################################################

import time, datetime

class SensorValue (object):
    class Types:
        """enum for sensor types"""
        Temp, Humi, Pressure, Switch = range(4)

    def __init__ (self, v_id, name, kind, unit):
        self.__v_id      = v_id
        self.__name      = name
        self.__kind      = kind
        self.__value     = None
        self.__unit      = unit
        self.__timestamp = None
        self.value       = "n/a"

    @property
    def value (self):
        if self.timestamp + 300.0 < time.time():
            return "n/a"  # data is older than 5 minutes
        else:
            return "%s %s" % (self.__value, self.unit)

    @value.setter
    def value (self, v):
        self.__value     = v
        self.__timestamp = time.time()

    @property
    def valuenumber (self):
        """returns value regardless of timestamp"""
        return self.__value

    @property
    def unit (self):
        """returns unit of measurement regardless of timestamp"""
        return self.__unit

    @property
    def timestamp (self):
        """returns timestamp of measurement"""
        return self.__timestamp

    @property
    def id (self):
        """returns ID of measurement"""
        return self.__v_id

    def __str__ (self):
        return "ID:        %s" % self.id        + "\n" + \
               "Name:      %s" % self.__name    + "\n" + \
               "Kind:      %s" % self.__kind    + "\n" + \
               "Value:     %s" % self.value     + "\n" + \
               "Unit:      %s" % self.unit      + "\n" + \
               "Timestamp: %s" % self.timestamp + "\n" + \
               "Timestamp: %s" % datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')


class SensorValueLock (object):
    def __init__ (self, v_id, name, kind, unit, lock):
        self._lock = lock
        self._sensorvalue = SensorValue(v_id, name, kind, unit)

    @property
    def value (self):
        with self._lock:
            return self._sensorvalue.value

    @value.setter
    def value (self, v):
        v = v.replace('.', ',')
        with self._lock:
            self._sensorvalue.value = v

# eof

