################################################################################
# SensorValue.py                                                               #
# Class providing various data of sensors                                      #
# (c) https://github.com/thomaspfeiffer-git 2016                               #
################################################################################


import time, datetime

class SensorValue (object):
    def __init__ (self, name, kind):
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
        self.__timestamp = time.time()

    def __str__ (self):
        return "Name:      %s" % self.__name      + "\n" + \
               "Kind:      %s" % self.__kind      + "\n" + \
               "Value:     %s" % self.__value     + "\n" + \
               "Timestamp: %s" % self.__timestamp + "\n" + \
               "Timestamp: %s" % datetime.datetime.fromtimestamp(self.__timestamp).strftime('%Y-%m-%d %H:%M:%S')

# eof

