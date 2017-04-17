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
from SensorQueue2 import SensorQueueClient_read

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

    def run (self):
        self.__running = True
        while self.__running:
            now = datetime.now()
            self.date_date.set(self.datestr(now))
            self.date_time.set(now.strftime("%X"))
            time.sleep(0.3)

    def stop (self):
        self.__running = False


###############################################################################
# Values ######################################################################
class Values (threading.Thread):
    """dedicated thread for updating all weather items"""
    def __init__ (self):
        threading.Thread.__init__(self)
        self.queue = SensorQueueClient_read("../config.ini")
        self.values = { "ID_{:02d}".format(id+1): None for id in range(40) }
        self.values.update({ "ID_OWM_{:02d}".format(id+1): None for id in range(30) })
                                                # some local calculated values
        self.values.update({ "ID_LC_{:02d}".format(id+1): None for id in range(30) })
        self.__running = False

    def init_values (self):
        for id in self.values.keys():
            self.values[id] = tk.StringVar()
            self.values[id].set(self.getvalue(None))

    @staticmethod
    def getvalue (sensorvalue):
        """returns measured value of sensor or "n/a" if sensorvalue == None"""
        return sensorvalue.value if sensorvalue is not None else "(n/a)"

    def calculate_local_values (self):
        """some tk.StringVar() values are calculated locally, eg compiled
           from several OpenWeatherMap data"""
        self.values['ID_LC_01'].set("Wettervorhersage aktuell:")
        self.values['ID_LC_02'].set("{} - {}".format(self.values['ID_OWM_01'].get(),
                                                     self.values['ID_OWM_02'].get()))
        self.values['ID_LC_03'].set("{} ({})".format(self.values['ID_OWM_03'].get(),
                                                     self.values['ID_OWM_04'].get()))

        title = "Wettervorhersage heute:" if datetime.now().hour < 12 else "Wettervorhersage morgen:"
        self.values['ID_LC_11'].set(title)
        self.values['ID_LC_12'].set("{} - {}".format(self.values['ID_OWM_11'].get(),
                                                     self.values['ID_OWM_12'].get()))
        self.values['ID_LC_13'].set("{} ({})".format(self.values['ID_OWM_13'].get(),
                                                     self.values['ID_OWM_14'].get()))

        title = "Wettervorhersage morgen:" if datetime.now().hour < 12 else "Wettervorhersage übermorgen:"
        self.values['ID_LC_21'].set(title)
        self.values['ID_LC_22'].set("{} - {}".format(self.values['ID_OWM_21'].get(),
                                                     self.values['ID_OWM_22'].get()))
        self.values['ID_LC_23'].set("{} ({})".format(self.values['ID_OWM_23'].get(),
                                                     self.values['ID_OWM_24'].get()))

    def run (self):
        self.__running = True
        newvalues = False
        while self.__running:
            v = self.queue.read()
            if v is not None: 
                self.values[v.id].set(self.getvalue(v))
                newvalues = True
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

# eof #

