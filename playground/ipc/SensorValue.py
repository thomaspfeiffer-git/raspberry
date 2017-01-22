################################################################################
# SensorValue.py                                                               #
# Class providing various data of sensors                                      #
# (c) https://github.com/thomaspfeiffer-git 2016                               #
################################################################################

from time import time, strftime, localtime

class SensorValue (object):
    def __init__ (self, v_id, name, kind):
        self.__v_id      = v_id
        self.__name      = name
        self.__kind      = kind
        self.__value     = None
        self.__timestamp = None

    @property
    def value (self):
        return self.__value

    @value.setter
    def value (self, v):
        self.__value     = v
        self.__timestamp = time()

    def getID (self):
        return self.__v_id

    def __str__ (self):
        return "ID:        %s" % self.getID()     + "\n" + \
               "Name:      %s" % self.__name      + "\n" + \
               "Kind:      %s" % self.__kind      + "\n" + \
               "Value:     %s" % self.__value     + "\n" + \
               "Timestamp: %s" % self.__timestamp + "\n" + \
               "Timestamp: {}".format(strftime("%Y%m%d %X",localtime(self.__timestamp)))

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
        with self.lock:
             self.sensorvalue.value = v


# eof

