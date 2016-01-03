class SensorValue (object):
    def __init__ (self, name, kind):
        self.__name = name
        self.__kind = kind

    def setValue (self, value):
        self.__value = value

    def showContent (self):
        print "Name:", self.__value
        print "Kind:", self.__kind
        print "Value:", self.__value

# eof

