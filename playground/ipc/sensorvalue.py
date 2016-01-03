import time, datetime

class SensorValue (object):
    def __init__ (self, name, kind):
        self.__name = name
        self.__kind = kind

    def setValue (self, value):
        self.__value     = value
        self.__timestamp = time.time()

    def showContent (self):
        print "Name:", self.__name
        print "Kind:", self.__kind
        print "Value:", self.__value
        print "Timestamp:", self.__timestamp
        print "Timestamp:", datetime.datetime.fromtimestamp(self.__timestamp).strftime('%Y-%m-%d %H:%M:%S')

# eof

