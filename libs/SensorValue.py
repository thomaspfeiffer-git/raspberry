# -*- coding: utf-8 -*-
################################################################################
# SensorValue.py                                                               #
# Class providing various data of sensors                                      #
# (c) https://github.com/thomaspfeiffer-git 2016                               #
################################################################################

import time, datetime

class SensorValue (object):
    def __init__ (self, v_id, name, kind, unit="XX"):
        self.__v_id      = v_id
        self.__name      = name
        self.__kind      = kind
        self.__value     = None
        self.__unit      = unit
        self.__timestamp = None
        self.value       = "n/a"

    @property
    def value (self):
        if self.getTimestamp() + 300.0 < time.time():
            return "n/a"  # data is older than 5 minutes
        else:
            return "%s %s" % (self.__value, self.__unit)

    @value.setter
    def value (self, v):
        self.__value     = v
        self.__timestamp = time.time()

    def getValue (self):
        """returns value regardless of timestamp"""
        return self.__value

    def getTimestamp (self):
        return self.__timestamp

    def getID (self):
        return self.__v_id

    def __str__ (self):
        return "ID:        %s" % self.getID()     + "\n" + \
               "Name:      %s" % self.__name      + "\n" + \
               "Kind:      %s" % self.__kind      + "\n" + \
               "Value:     %s" % self.__value     + "\n" + \
               "Unit:      %s" % self.__unit      + "\n" + \
               "Timestamp: %s" % self.__timestamp + "\n" + \
               "Timestamp: %s" % datetime.datetime.fromtimestamp(self.__timestamp).strftime('%Y-%m-%d %H:%M:%S')


class SensorValueLock (object):
    def __init__ (self, v_id, name, kind, lock):
        self.lock = lock
        self.sensorvalue = SensorValue(v_id, name, kind)

    @property
    def value (self):
        with self.lock:
            return self.sensorvalue.value

    @value.setter
    def value (self, v):
        v = v.replace('.', ',')
        with self.lock:
            self.sensorvalue.value = v


# eof

