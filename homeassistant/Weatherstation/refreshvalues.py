# -*- coding: utf-8 -*-
############################################################################
# refreshvalues.py                                                         #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""updates all variable values of the screens:
   - Clock: all date/time items updated in a dedicated thread.
   - Values: all weather values updated in a dedicated thread.
             all these values are read from the queue provided
             by the SensorQueue.
"""

from datetime import datetime
import sys
import threading
import time
import tkinter as tk

sys.path.append('../../libs')
from Logging import Log

sys.path.append("../Queueserver/")
from SensorQueue import SensorQueueClient_read

from config import CONFIG
from constants import CONSTANTS


###############################################################################
# Clock #######################################################################
class Clock (threading.Thread):
    """dedicated thread for updating the date and time fields"""
    def __init__ (self):
        threading.Thread.__init__(self)
        self.__running = False

    def init_values (self):
        self.date_date = tk.StringVar()
        self.date_time = tk.StringVar()

    @staticmethod
    def datestr (now):
        return "{}, {}. {} {}".format(CONSTANTS.DAYOFWEEK[now.weekday()], now.day,
                                      CONSTANTS.MONTHNAMES[now.month], now.year)

    @staticmethod
    def timestr (now):
        return f"{now.hour}:{now.minute:02d}:{now.second:02d}"

    def run (self):
        self.__running = True
        while self.__running:
            now = datetime.now()
            self.date_date.set(self.datestr(now))
            self.date_time.set(self.timestr(now))
            time.sleep(0.2)

    def stop (self):
        self.__running = False


###############################################################################
# A_Value #####################################################################
class A_Value (object):
    def __init__ (self):
        self.tk_StringVar = None
        self.valid_until = float('inf')


###############################################################################
# Values ######################################################################
class Values (threading.Thread):
    """dedicated thread for updating all weather items"""
    def __init__ (self):
        threading.Thread.__init__(self)
        self.queue = SensorQueueClient_read("../config.ini")
        self.values = { "ID_{:02d}".format(id+1): A_Value() for id in range(60) }
        self.values.update({ "ID_OWM_{:02d}".format(id+1): A_Value() for id in range(30) })
                                                # some local calculated values
        self.values.update({ "ID_LC_{:02d}".format(id+1): A_Value() for id in range(30) })
        self.values.update({ "ID_AW_{:02d}".format(id+1): A_Value() for id in range(10) })
        self.__running = False

    def init_values (self):
        for id in self.values.keys():
            self.values[id].tk_StringVar = tk.StringVar()
            self.values[id].tk_StringVar.set(self.getvalue(None))

    @staticmethod
    def getvalue (sensorvalue):
        """returns measured value of sensor or "n/a" if sensorvalue == None"""
        return sensorvalue.value if sensorvalue is not None else "(n/a)"

    def calculate_local_values (self):
        """some tk.StringVar() values are calculated locally, eg compiled
           from several OpenWeatherMap data"""
        self.values['ID_LC_01'].tk_StringVar.set("Wettervorhersage aktuell:")
        self.values['ID_LC_02'].tk_StringVar.set("{} - {}".format(self.values['ID_OWM_01'].tk_StringVar.get(),
                                                                  self.values['ID_OWM_02'].tk_StringVar.get()))
        self.values['ID_LC_03'].tk_StringVar.set("{} ({})".format(self.values['ID_OWM_03'].tk_StringVar.get(),
                                                                  self.values['ID_OWM_04'].tk_StringVar.get()))

        title = "Wettervorhersage heute:" if datetime.now().hour < 12 else "Wettervorhersage morgen:"
        self.values['ID_LC_11'].tk_StringVar.set(title)
        self.values['ID_LC_12'].tk_StringVar.set("{} - {}".format(self.values['ID_OWM_11'].tk_StringVar.get(),
                                                                  self.values['ID_OWM_12'].tk_StringVar.get()))
        self.values['ID_LC_13'].tk_StringVar.set("{} ({})".format(self.values['ID_OWM_13'].tk_StringVar.get(),
                                                                  self.values['ID_OWM_14'].tk_StringVar.get()))

        title = "Wettervorhersage morgen:" if datetime.now().hour < 12 else "Wettervorhersage übermorgen:"
        self.values['ID_LC_21'].tk_StringVar.set(title)
        self.values['ID_LC_22'].tk_StringVar.set("{} - {}".format(self.values['ID_OWM_21'].tk_StringVar.get(),
                                                                  self.values['ID_OWM_22'].tk_StringVar.get()))
        self.values['ID_LC_23'].tk_StringVar.set("{} ({})".format(self.values['ID_OWM_23'].tk_StringVar.get(),
                                                                  self.values['ID_OWM_24'].tk_StringVar.get()))

    def run (self):
        self.__running = True
        newvalues = False
        while self.__running:
            v = self.queue.read()
            if v is not None:
                # Log(f"Value received: {v}")
                try:
                    self.values[v.id].tk_StringVar.set(self.getvalue(v))
                    self.values[v.id].valid_until = time.time() + 180 # data is valid for 3 min
                    newvalues = True
                except KeyError:
                    Log("Error: Unknown id '{}'.".format(v.id))
            else:  # queue empty --> get some interruptible sleep
                if newvalues:
                   self.calculate_local_values()
                   newvalues = False
                for _ in range(10):
                   time.sleep(0.1)
                   if not self.__running:
                       break

    def stop (self):
        self.__running = False


###############################################################################
# OutOfService ################################################################
class OutOfService (threading.Thread):
    """ iterates over all Value.values and sets value to "n/a" if timestamp
        is older than n minutes"""
    def __init__ (self, values):
        threading.Thread.__init__(self)
        self.values = values
        self._running = True

    def run (self):
        while self._running:
            for id_ in self.values.values.keys():
                if self.values.values[id_].valid_until < time.time():
                    Log("Setting {} to NN/AA".format(id_))
                    self.values.values[id_].tk_StringVar.set("NN/AA")

            for _ in range(600):
                time.sleep(0.1)
                if not self._running:
                    break

    def stop (self):
        self._running = False

# eof #

