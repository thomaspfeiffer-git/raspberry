import datetime

class SensorValue (object):
    def __init__ (self, name, kind):
        self.__name = name
        self.__kind = kind

    def setValue (self, value):
        self.__value     = value
        self.__timestamp = datetime.datetime.now()

    def showContent (self):
        print "Name:", self.__name
        print "Kind:", self.__kind
        print "Value:", self.__value
        print "Timestamp:", self.__timestamp

# eof

