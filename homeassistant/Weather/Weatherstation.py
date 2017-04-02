#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# Weatherstation.py                                                           #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
###############################################################################
"""Weatherstation: collects various data from sensors in our flat and garden
   and displays them on a Touch Screen Display."""

### usage ###
# ./Weatherstation.py


### useful ressources ###
# turn off screen saver:
# sudo apt-get install xscreensaver
# start xscreensaver an set screensaver off manually
#
# Packages you might install
# sudo apt-get install python3-pil.imagetk
#
# Adjusting lightness
# cd /sys/class/backlight/rpi_backlight/
# sudo bash -c 'echo "255" > brightness'
# def _set_value(name, value):
#    with open(os.path.join(PATH, name), "w") as f:
#        f.write(str(value))
#


import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font
import PIL.Image
import PIL.ImageTk

from collections import OrderedDict
from datetime import datetime
import os
import sys
import threading
import time

sys.path.append('../../libs')
from SensorQueue2 import SensorQueueClient_read
from Shutdown import Shutdown

from Config import CONFIG
from Constants import CONSTANTS


class Displayelement (object):
    """provides the basic logic for calculating the grid pos of an element"""
    @property
    def gridpos (self):
        return self.__gridpos

    @gridpos.setter
    def gridpos (self, gridpos):
        self.__gridpos = gridpos


class Text (tk.Label, Displayelement):
    """prints text"""
    """update of data is done in stringvar (must be of type tk.StringVar)"""
    def __init__ (self, frame, gridpos, text, stringvar, anchor, sticky, font, color):
        # TODO: type safety: stringvar
        super().__init__(frame, text=text, textvariable=stringvar, 
                         # justify="left", anchor=anchor, font=font,
                         justify="center", anchor=anchor, font=font,
                         foreground=color, background=CONFIG.COLORS.BACKGROUND)
        self.gridpos = gridpos+1
        self.grid(row=gridpos, column=1, columnspan=5, sticky=sticky)


class WeatherItem (Text):
    """draws a single weather item"""
    def __init__ (self, frame, gridpos, stringvar, font=None, color=None):
        super().__init__(frame, gridpos=gridpos, text=None, stringvar=stringvar, 
                         anchor="w", sticky="w", font=font, color=color)


class DateItem (Text):
    """draws a date line"""
    def __init__ (self, frame, gridpos, stringvar, font, color):
        super().__init__(frame, gridpos=gridpos, text=None, stringvar=stringvar, 
                         anchor="center", sticky="we", font=font, color=color)


class SeparatorText (Text):
    """prints separator text"""
    def __init__ (self, frame, gridpos, text, font):
        super().__init__(frame, gridpos=gridpos, text=text, stringvar=None, 
                         anchor="w", sticky="we", font=font, color=CONFIG.COLORS.SEP)


class SeparatorLine (ttk.Separator, Displayelement):
    """prints separator line"""
    def __init__ (self, frame, gridpos):
        super().__init__(frame, orient="horizontal")
        self.gridpos = gridpos+1
        self.grid(row=gridpos, column=1, columnspan=5, sticky="we")


class Separator (Displayelement): 
    """prints a separator which consists of a line and some text"""
    def __init__ (self, frame, gridpos, text=None, font=None):
        self.gridpos = SeparatorLine(frame=frame, gridpos=gridpos).gridpos
        if text is not None:
            self.gridpos = SeparatorText(frame=frame, gridpos=self.gridpos,
                                         text=text, font=font).gridpos


###############################################################################
# Clock #######################################################################
class Clock (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self.__running = False

    def init_values (self, master):
        self.date_date = tk.StringVar(master)
        self.date_time = tk.StringVar(master)

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
    def __init__ (self):
        threading.Thread.__init__(self)
        self.queue = SensorQueueClient_read("../config.ini")
        self.values = { "ID_{:02d}".format(id+1): None for id in range(40) }
        self.values.update({ "ID_OWM_{:02d}".format(id+1): None for id in range(30) })
        self.__running = False

    def init_values (self, master):
        for id in self.values.keys():
            self.values[id] = tk.StringVar()
            self.values[id].set(self.getvalue(None))

    @staticmethod
    def getvalue (sensorvalue):
        """returns measured value of sensor or "n/a" if sensorvalue == None"""
        if sensorvalue is not None:
            return sensorvalue.value
        else:
            return "(n/a)"

    def run (self):
        self.__running = True
        while self.__running:
            v = self.queue.read()
            if v is not None: 
                self.values[v.id].set(self.getvalue(v))
            else:  # queue empty --> get some interruptible sleep
                for _ in range(100):
                    time.sleep(0.1)

    def stop (self):
        self.__running = False


###############################################################################
# WeatherApp ##################################################################
class WeatherApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.screennames = ['main', 'owm', 'kid']
        self.screenid = 0  # Number of currently displayed screen

        self.master = master

        clock.init_values(master)
        clock.start()
        values.init_values(master)
        values.start()

        family = "Arial" # TODO: get from config file
        self.font_item      = Font(family=family, size=CONFIG.FONTS.SIZE_NORMAL)
        self.font_separator = Font(family=family, size=CONFIG.FONTS.SIZE_TINY)
        self.font_date      = Font(family=family, size=CONFIG.FONTS.SIZE_SMALL)
        self.font_date_bold = Font(family=family, size=CONFIG.FONTS.SIZE_SMALL, weight="bold")

        self.grid()
        self.create_screens()
        self.create_dateframe(self.master)

        self.master.bind("<Button-1>", self.touch_event)


    def touch_event (self, event):
        self.screens[self.screennames[self.screenid]].grid_remove()
        self.screenid += 1
        if self.screenid >= len(self.screennames): 
            self.screenid = 0
        self.screens[self.screennames[self.screenid]].grid()


    def create_screens (self):
        self.screens = OrderedDict()
        for screen in self.screennames:
            self.screens[screen] = tk.Frame(self)
            self.screens[screen].config(bd=10, bg=CONFIG.COLORS.BACKGROUND, 
                                        width=self.master.width, height=410)
            self.screens[screen].grid_propagate(0)
            getattr(self, "create_screen_{}".format(screen))() # call create_screen_X()

        self.screens['main'].grid()


    def create_dateframe (self, master):
        self.dateframe = tk.Frame(master)
        self.dateframe.config(bd=10, bg=CONFIG.COLORS.BACKGROUND, 
                              width=self.master.width, height=70)
        self.dateframe.grid_propagate(0)
        self.dateframe.grid()

        gridpos = 0
        gridpos = Separator(frame=self.dateframe, gridpos=gridpos).gridpos
        gridpos = DateItem(frame=self.dateframe, gridpos=gridpos, 
                           stringvar=clock.date_date,
                           font=self.font_date, color=CONFIG.COLORS.DATE).gridpos
        gridpos = DateItem(frame=self.dateframe, gridpos=gridpos, 
                           stringvar=clock.date_time,
                           font=self.font_date_bold, color=CONFIG.COLORS.DATE).gridpos


    def create_screen_main (self):
        frame = self.screens['main']
        gridpos = 0

        icon = PIL.Image.open("../Resources/ico_sunny.png")
        icon = icon.resize((40, 40),  PIL.Image.ANTIALIAS)
        self.icon = PIL.ImageTk.PhotoImage(icon)

        icons = [i for i in range(5)]
        for i in range(len(icons)):
            icons[i] = tk.Label(frame, image=self.icon, 
                                height=50, bg=CONFIG.COLORS.BACKGROUND)
            icons[i].grid(row=gridpos, column=i+1)
        gridpos += 1

        gridpos = Separator(frame=frame, gridpos=gridpos, text="Wohnzimmer:", 
                            font=self.font_separator).gridpos
        gridpos = WeatherItem(frame=frame, gridpos=gridpos, 
                              stringvar=values.values['ID_01'],
                              font=self.font_item, color=CONFIG.COLORS.INDOOR).gridpos
        gridpos = WeatherItem(frame=frame, gridpos=gridpos, 
                              stringvar=values.values['ID_02'],
                              font=self.font_item, color=CONFIG.COLORS.INDOOR).gridpos

        gridpos = Separator(frame=frame, gridpos=gridpos, text="Draußen:", 
                            font=self.font_separator).gridpos
        gridpos = WeatherItem(frame=frame, gridpos=gridpos, 
                              stringvar=values.values['ID_12'],
                              font=self.font_item, color=CONFIG.COLORS.OUTDOOR).gridpos
        gridpos = WeatherItem(frame=frame, gridpos=gridpos, 
                              stringvar=values.values['ID_04'],
                              font=self.font_item, color=CONFIG.COLORS.OUTDOOR).gridpos
        gridpos = WeatherItem(frame=frame, gridpos=gridpos, 
                              stringvar=values.values['ID_05'],
                              font=self.font_item, color=CONFIG.COLORS.OUTDOOR).gridpos


    def create_screen_owm (self):
        gridpos = 0
        gridpos = Separator(frame=self.screens['owm'], gridpos=gridpos, 
                            text="Wettervorhersage aktuell:", 
                            font=self.font_separator).gridpos
        gridpos = WeatherItem(frame=self.screens['owm'], gridpos=gridpos, 
                              stringvar=values.values['ID_OWM_01'],
                              font=self.font_item, color=CONFIG.COLORS.FORECAST).gridpos
        gridpos = WeatherItem(frame=self.screens['owm'], gridpos=gridpos, 
                              stringvar=values.values['ID_OWM_01'],
                              font=self.font_item, color=CONFIG.COLORS.FORECAST).gridpos


    def create_screen_kid (self):
        gridpos = 0
        gridpos = Separator(frame=self.screens['kid'], gridpos=gridpos, 
                            text="Kinderzimmer:", 
                            font=self.font_separator).gridpos
        gridpos = WeatherItem(frame=self.screens['kid'], gridpos=gridpos, 
                              stringvar=values.values['ID_06'],
                              font=self.font_item, color=CONFIG.COLORS.KIDSROOM).gridpos
        gridpos = WeatherItem(frame=self.screens['kid'], gridpos=gridpos, 
                              stringvar=values.values['ID_06'],
                              font=self.font_item, color=CONFIG.COLORS.KIDSROOM).gridpos


###############################################################################
# Weather #####################################################################
class Weather (object):
    """manages tk's root window"""
    def __init__ (self):
        self.root = tk.Tk()
        self.root.overrideredirect(1)

        self.root.resizable(width=False, height=False)
        # w = self.root.winfo_screenwidth() # TODO Get coordinates from config file
        w = 280 # TODO beautify code
        h = self.root.winfo_screenheight()
        self.root.width = 280
        self.root.height = self.root.winfo_screenheight()
        # print("w: {}, h: {}".format(w, h))
        self.root.geometry("{}x{}+{}+{}".format(w,h,0,0))
        self.root.config(bg=CONFIG.COLORS.BACKGROUND)
        self.app = WeatherApp(master=self.root)

    def poll (self):
        """polling needed for ctrl-c"""
        self.root.after(50, self.poll)

    def run (self):
        """start polling and run application"""
        self.root.after(50, self.poll)
        self.app.mainloop()

    def stop (self):
        """stops application, called on shutdown"""
        self.root.destroy()
        self.root.quit() # TODO: check usage of destroy() and quit()


###############################################################################
# shutdown_application ########################################################
def shutdown_application ():
    """called on shutdown; stops all threads"""
    print("in shutdown_application()")
    clock.stop()
    clock.join()
    values.stop()
    values.join()
    weather.stop()
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    # TODO: if $DISPLAY == "": default setting = ":0.0"
    os.environ["DISPLAY"] = ":0.0"
    shutdown = Shutdown(shutdown_func=shutdown_application)

    values = Values()
    clock  = Clock()

    weather = Weather()
    weather.run()

"""
    # make separate thread
    sensorqueue = SensorQueueClient_read("../config.ini")
    while True:
"""

# eof #

