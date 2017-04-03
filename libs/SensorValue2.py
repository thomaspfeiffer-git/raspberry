# -*- coding: utf-8 -*-
################################################################################
# SensorValue.py                                                               #
# Class providing various data of sensors                                      #
# (c) https://github.com/thomaspfeiffer-git 2016, 2017                         #
################################################################################
"""provides classes for:
   SensorValue: measured values including a timestamp of all weather sensors
   SensorValueLock: Wraps SensorValue read and write access with a Lock.
"""

from time import time, strftime, localtime


class SensorValue_Data (object):
    """contains various data of measured values"""
    class Types:
        """enum for sensor types"""
        Temp, Humi, Pressure, Switch, Light, Wind, WindDir, Desc, IconUrl = range(9)

    def __init__ (self, v_id, name, type_, unit):
        self.__v_id      = v_id
        self.__name      = name
        self.__type      = type_
        self.__value     = None
        self.__unit      = unit
        self.__timestamp = None
        self.value       = "n/a"

    @property
    def value (self):
        """returns the measured value as string including unit of
           measurement; eg: "13,4 °C" (please note the decimal coma here)"""
        if (self.timestamp + 300.0 < time()):
            return "n/a"  # data is older than 5 minutes
        else:
            if (self.type_ == SensorValue_Data.Types.Switch):
                return "%s %s" % (self.unit, self.__value)
            elif self.__unit:
                return "%s %s" % (self.__value, self.unit)
            else:
                return "%s" % (self.__value)

    @value.setter
    def value (self, _value):
        """sets the value of measurement"""
        if self.__type in (SensorValue_Data.Types.Temp, SensorValue_Data.Types.Humi, 
                           SensorValue_Data.Types.Pressure, SensorValue_Data.Types.Light,
                           SensorValue_Data.Types.Wind):
            """please note the decimal coma here"""
            _value = _value.replace('.', ',')
        self.__value     = _value
        self.__timestamp = time()

    @property
    def valuenumber (self):
        """returns value regardless of timestamp"""
        return self.__value

    @property
    def id (self):
        """returns ID of measurement"""
        return self.__v_id

    @property
    def type_ (self):
        """returns type of sensor"""
        return self.__type

    @property
    def unit (self):
        """returns unit of measurement regardless of timestamp"""
        return self.__unit

    @property
    def timestamp (self):
        """returns timestamp of measurement"""
        return self.__timestamp

    def __str__ (self):
        return "ID:        %s" % self.id        + "\n" + \
               "Name:      %s" % self.__name    + "\n" + \
               "Type:      %s" % self.type_     + "\n" + \
               "Value:     %s" % self.value     + "\n" + \
               "Unit:      %s" % self.unit      + "\n" + \
               "Timestamp: %s" % self.timestamp + "\n" + \
               "Timestamp: {}".format(strftime("%Y%m%d %X",localtime(self.__timestamp)))


class SensorValue (object):
    # TODO change doc string
    """Provides a wrapper for a SensorValue with a Lock(). 
       Locks cannot be pickled, therefore we need to use a dedicated
       class for SensorValues with Locks"""
    def __init__ (self, v_id, name, type_, unit):
        self.__queuefunc = None
        self._sensorvalue = SensorValue_Data(v_id, name, type_, unit)

    def setqueuefunc (self, func):
        """sets the queuefunc; queuefunc() is called when the calue is set
           signature of queuefunc(): queuefunc(sensorvalue)
           where sensorvalue is of type SensorValue
           queuefunc() is used to write data into a queue"""
        self.__queuefunc = func
        print("setqueuefunc: {}".format(self.__queuefunc))

    @property
    def value (self):
        return self._sensorvalue.value

    @value.setter
    def value (self, _value):
        self._sensorvalue.value = _value
        # print("value, __queuefunc: {}".format(self.__queuefunc))
        if self.__queuefunc is not None:  # value() is called in constructor as well
            self.__queuefunc(self._sensorvalue)   # TODO: set __queuefunc in Constructor?

# eof

