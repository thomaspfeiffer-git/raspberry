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


import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font

import os
import sys


sys.path.append('../../libs')
from SensorQueue2 import SensorQueueClient_read
from Shutdown import Shutdown

from Config import CONFIG


class Displayelement (object):
    @property
    def gridpos (self):
        return self.__gridpos

    @gridpos.setter
    def gridpos (self, gridpos):
        self.__gridpos = gridpos


class Text (tk.Label, Displayelement):
    """prints text"""
    """update of data is done in stringvar (must be of type tk.StringVar)"""
    def __init__ (self, frame, gridpos, text, stringvar, sticky, font, color):
        # TODO: type safety: stringvar
        super().__init__(frame, text=text, textvariable=stringvar, 
                         justify="left", anchor="w", font=font,
                         foreground=color, background=CONFIG.COLORS.BACKGROUND)
        self.gridpos = gridpos+1
        self.grid(row=gridpos, column=1, sticky=sticky)


class WeatherItem (Text):
    """draws a single weather item"""
    def __init__ (self, frame, gridpos, stringvar, font, color):
        super().__init__(frame, gridpos=gridpos, text=None, stringvar=stringvar, 
                         sticky="w", font=font, color=color)


class DateItem (Text):
    """draws a date line"""
    def __init__ (self, frame, gridpos, stringvar, font, color):
        super().__init__(frame, gridpos=gridpos, text=None, stringvar=stringvar, 
                         sticky="n", font=font, color=color)


class SeparatorText (Text):
    """prints separator text"""
    def __init__ (self, frame, gridpos, text, font):
        super().__init__(frame, gridpos=gridpos, text=text, stringvar=None, 
                         sticky="w", font=font, color=CONFIG.COLORS.SEP)


class SeparatorLine (ttk.Separator, Displayelement):
    """prints separator line"""
    def __init__ (self, frame, gridpos):
        super().__init__(frame, orient="horizontal")
        self.gridpos = gridpos+1
        self.grid(row=gridpos, column=1, sticky="ew")


class Separator (Displayelement): 
    """prints a separator which consists of a line and some text"""
    def __init__ (self, frame, gridpos, text=None, font=None):
        self.gridpos = SeparatorLine(frame=frame, gridpos=gridpos).gridpos
        if text is not None:
            self.gridpos = SeparatorText(frame=frame, gridpos=self.gridpos,
                                         text=text, font=font).gridpos


###############################################################################
# WeatherApp ##################################################################
class WeatherApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)
        self.master = master
        self.config(bg=CONFIG.COLORS.BACKGROUND)

        self.font_item      = Font(family="Helvetica", size=CONFIG.FONTS.SIZE_NORMAL)
        self.font_separator = Font(family="Helvetica", size=CONFIG.FONTS.SIZE_TINY)
        self.font_date      = Font(family="Helvetica", size=CONFIG.FONTS.SIZE_SMALL)
        self.font_date_bold = Font(family="Helvetica", size=CONFIG.FONTS.SIZE_SMALL, weight="bold")

        self.pack()
        self.create_widgets()

    def create_widgets (self):
        self.grid()
        frame = tk.Frame(self, bd=10, bg=CONFIG.COLORS.BACKGROUND, width=400)
        frame.grid()
        gridpos = 1
 
        temp_indoor = tk.StringVar()
        humi_indoor = tk.StringVar()
        temp_outdoor = tk.StringVar()
        humi_outdoor = tk.StringVar()
        pressure_outdoor = tk.StringVar()

        date_date = tk.StringVar()
        date_time = tk.StringVar()

        temp_indoor.set("23,7 °C")
        humi_indoor.set("47,56 % rF")
        temp_outdoor.set("-4,3 °C")
        humi_outdoor.set("67,99 % rF")
        pressure_outdoor.set("1013,2  hPa")

        from datetime import datetime
        now = datetime.now()
        date_date.set(now.strftime("%A, %d. %B %Y"))
        date_time.set(now.strftime("%X"))
 
        gridpos = Separator(frame=frame, gridpos=gridpos, text="Wohnzimmer:", 
                       font=self.font_separator).gridpos
        gridpos = WeatherItem(frame=frame, gridpos=gridpos, stringvar=temp_indoor, 
                              font=self.font_item, color=CONFIG.COLORS.INDOOR).gridpos
        gridpos = WeatherItem(frame=frame, gridpos=gridpos, stringvar=humi_indoor, 
                              font=self.font_item, color=CONFIG.COLORS.INDOOR).gridpos

        gridpos = Separator(frame=frame, gridpos=gridpos, text="Draußen:", 
                            font=self.font_separator).gridpos
        gridpos = WeatherItem(frame=frame, gridpos=gridpos, stringvar=temp_outdoor, 
                              font=self.font_item, color=CONFIG.COLORS.OUTDOOR).gridpos
        gridpos = WeatherItem(frame=frame, gridpos=gridpos, stringvar=humi_outdoor, 
                              font=self.font_item, color=CONFIG.COLORS.OUTDOOR).gridpos
        gridpos = WeatherItem(frame=frame, gridpos=gridpos, stringvar=pressure_outdoor,
                              font=self.font_item, color=CONFIG.COLORS.OUTDOOR).gridpos

        gridpos = Separator(frame=frame, gridpos=gridpos).gridpos
        gridpos = DateItem(frame=frame, gridpos=gridpos, stringvar=date_date,
                           font=self.font_date, color=CONFIG.COLORS.DATE).gridpos
        gridpos = DateItem(frame=frame, gridpos=gridpos, stringvar=date_time,
                           font=self.font_date_bold, color=CONFIG.COLORS.DATE).gridpos


###############################################################################
# Weather #####################################################################
class Weather (object):
    """manages tk's root window"""
    def __init__ (self):
        self.root = tk.Tk()
        self.root.overrideredirect(1)

        self.root.resizable(width=False, height=False)
        # w = self.root.winfo_screenwidth() // 2
        w = 280
        h = self.root.winfo_screenheight()
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


# shutdown_application ########################################################
def shutdown_application ():
    """called on shutdown; stops all threads"""
    print("in shutdown_application()")
    weather.stop()
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    # TODO: if $DISPLAY == "": default setting = ":0.0"
    os.environ["DISPLAY"] = ":0.0"
    shutdown = Shutdown(shutdown_func=shutdown_application)

    weather = Weather()
    weather.run()

"""
    # make separate thread
    sensorqueue = SensorQueueClient_read("../config.ini")
    while True:
        v = sensorqueue.read()
        if v is not None: 
            print(v)
"""

# eof #

