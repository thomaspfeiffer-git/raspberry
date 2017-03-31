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
# http://www.etcwiki.org/wiki/Disable_screensaver_and_screen_blanking_Raspberry_Pi
# http://raspberrypi.stackexchange.com/questions/752/how-do-i-prevent-the-screen-from-going-blank
#
# sudo apt-get install xscreensaver



import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font

import os
import sys


sys.path.append('../../libs')
from SensorQueue2 import SensorQueueClient_read
from Shutdown import Shutdown

from Config import CONFIG


class Item (tk.Label):
    """draws a single weather item
       update of data is done in stringvar (must be of type tk.StringVar)"""
    def __init__ (self, frame, gridpos, stringvar, font, color):
        # TODO: type safety: stringvar
        super().__init__(frame, textvariable=stringvar, 
                         justify="left", anchor="w", font=font,
                         foreground=color, background=CONFIG.COLORS.BACKGROUND)
        self.__nextgridpos = gridpos+1
        self.grid(row=gridpos, column=1, sticky="w")

    def nextgridpos (self):
        return self.__nextgridpos


class SeparatorText (tk.Label):
    """print separator text"""
    def __init__ (self, frame, gridpos, text, font):
        super().__init__(frame, text=text, justify="left", anchor="w", font=font,
                         fg=CONFIG.COLORS.SEP, bg=CONFIG.COLORS.BACKGROUND)
        self.__nextgridpos = gridpos+1
        self.grid(row=gridpos, column=1, sticky="w")

    def nextgridpos (self):
        return self.__nextgridpos


class SeparatorLine (ttk.Separator):
    """print separator line"""
    def __init__ (self, frame, gridpos):
        super().__init__(frame, orient="horizontal")
        self.__nextgridpos = gridpos+1
        self.grid(row=gridpos, column=1, sticky="ew")

    def nextgridpos (self):
        return self.__nextgridpos


class Separator (object): 
    """prints a separator which consists of a line and some text"""
    def __init__ (self, frame, gridpos, text=None, font=None):
        gridpos = SeparatorLine(frame=frame, gridpos=gridpos).nextgridpos()
        self.__nextgridpos = gridpos
        if text is not None:
            gridpos = SeparatorText(frame=frame, gridpos=self.nextgridpos(), 
                                    text=text, font=font).nextgridpos()
            self.__nextgridpos = gridpos+1

    def nextgridpos (self):
        return self.__nextgridpos


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
        frame = tk.Frame(self, bd=10, bg=CONFIG.COLORS.INDOOR, width=400)
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
                       font=self.font_separator).nextgridpos()
        gridpos = Item(frame=frame, gridpos=gridpos, stringvar=temp_indoor, 
                       font=self.font_item, color=CONFIG.COLORS.INDOOR).nextgridpos()
        gridpos = Item(frame=frame, gridpos=gridpos, stringvar=humi_indoor, 
                       font=self.font_item, color=CONFIG.COLORS.INDOOR).nextgridpos()

        gridpos = Separator(frame=frame, gridpos=gridpos, text="Draußen:", 
                       font=self.font_separator).nextgridpos()
        gridpos = Item(frame=frame, gridpos=gridpos, stringvar=temp_outdoor, 
                       font=self.font_item, color=CONFIG.COLORS.OUTDOOR).nextgridpos()
        gridpos = Item(frame=frame, gridpos=gridpos, stringvar=humi_outdoor, 
                       font=self.font_item, color=CONFIG.COLORS.OUTDOOR).nextgridpos()
        gridpos = Item(frame=frame, gridpos=gridpos, stringvar=pressure_outdoor,
                       font=self.font_item, color=CONFIG.COLORS.OUTDOOR).nextgridpos()

        gridpos = Separator(frame=frame, gridpos=gridpos).nextgridpos()
        gridpos = Item(frame=frame, gridpos=gridpos, stringvar=date_date,
                       font=self.font_date, color=CONFIG.COLORS.DATE).nextgridpos()
        gridpos = Item(frame=frame, gridpos=gridpos, stringvar=date_time,
                       font=self.font_date_bold, color=CONFIG.COLORS.DATE).nextgridpos()


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

