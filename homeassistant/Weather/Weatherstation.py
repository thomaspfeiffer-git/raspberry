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
# Change of screen
# grid_forget()
# http://effbot.org/tkinterbook/grid.htm#Tkinter.Grid.grid_forget-method
# http://stackoverflow.com/questions/12364981/how-to-delete-tkinter-widgets-from-a-window


import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font
import PIL.Image
import PIL.ImageTk

from datetime import datetime
import os
import sys
import threading
import time

sys.path.append('../../libs')
from SensorQueue2 import SensorQueueClient_read
from Shutdown import Shutdown

from Config import CONFIG


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
    def __init__ (self, frame, gridpos, text, stringvar, sticky, font, color):
        # TODO: type safety: stringvar
        super().__init__(frame, text=text, textvariable=stringvar, 
                         justify="left", anchor="w", font=font,
                         relief="raised",
                         foreground=color, background=CONFIG.COLORS.BACKGROUND)
        self.gridpos = gridpos+1
        self.grid(row=gridpos, column=1, columnspan=5, sticky=sticky)


class WeatherItem (Text):
    """draws a single weather item"""
    def __init__ (self, frame, gridpos, stringvar, font=None, color=None):
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
        self.grid(row=gridpos, column=1, columnspan=5, sticky="ew")


class Separator (Displayelement): 
    """prints a separator which consists of a line and some text"""
    def __init__ (self, frame, gridpos, text=None, font=None):
        self.gridpos = SeparatorLine(frame=frame, gridpos=gridpos).gridpos
        if text is not None:
            self.gridpos = SeparatorText(frame=frame, gridpos=self.gridpos,
                                         text=text, font=font).gridpos



###############################################################################
# Values ######################################################################
class Values (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self.__running = False

    def init_values (self, master):
        self.date_date = tk.StringVar(master)
        self.date_time = tk.StringVar(master)

    def run (self):
        self.__running = True
        while self.__running:
            now = datetime.now()
            self.date_date.set(now.strftime("%A, %d. %B %Y"))
            self.date_time.set(now.strftime("%X"))
            time.sleep(0.5)

    def stop (self):
        self.__running = False



def hallo (event):
    print("Event: touched")


###############################################################################
# WeatherApp ##################################################################
class WeatherApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.screenid = 0

        self.master = master
        self.config(bg=CONFIG.COLORS.BACKGROUND)

        values.init_values(master)
        values.start()

        self.font_item      = Font(family="Helvetica", size=CONFIG.FONTS.SIZE_NORMAL)
        self.font_separator = Font(family="Helvetica", size=CONFIG.FONTS.SIZE_TINY)
        self.font_date      = Font(family="Helvetica", size=CONFIG.FONTS.SIZE_SMALL)
        self.font_date_bold = Font(family="Helvetica", size=CONFIG.FONTS.SIZE_SMALL, weight="bold")

        self.pack()

        # http://www.python-course.eu/tkinter_events_binds.php
        master.bind("<Button-1>", hallo)
        # master.bind("<Button-1>", self.touch_event)

        self.create_widgets()

    def touch_event (event):
        self.screenid += 1
        if self.screenid >= 5: self.screenid = 0
        print("WeatherApp.touch_event, screenid: {}".format(self.screenid))


    def create_widgets (self):
        self.grid()
        frame = tk.Frame(self, bd=10, bg=CONFIG.COLORS.BACKGROUND, width=400)
        frame.grid()
        gridpos = 1

        self.frame_array = [ frame,
                             tk.Frame(self, bd=10, bg=CONFIG.COLORS.INDOOR, width=400),
                             tk.Frame(self, bd=10, bg=CONFIG.COLORS.OUTDOOR, width=400) ]


        # test 1
        # on event click:
        #    self.frame_array[0].grid_remove()
        #    print("removed")
        # on second event click:
        #    self.frame_array[0].grid()
        #    print("grid added")
        

        # i = 0
        # on event click:
        #    self.frame_array[i].grid_remove()
        #    i += 1
        #    if >= 3: i = 0
        #    self.frame_array[i].grid()

 
        temp_indoor = tk.StringVar()
        humi_indoor = tk.StringVar()
        temp_outdoor = tk.StringVar()
        humi_outdoor = tk.StringVar()
        pressure_outdoor = tk.StringVar()

        temp_indoor.set("23,7 °C")
        humi_indoor.set("47,56 % rF")
        temp_outdoor.set("-4,3 °C")
        humi_outdoor.set("67,99 % rF")
        pressure_outdoor.set("1013,2  hPa")

        icon = PIL.Image.open("../Resources/ico_sunny.png")
        icon = icon.resize((40, 40),  PIL.Image.ANTIALIAS)
        self.icon = PIL.ImageTk.PhotoImage(icon)
        x = tk.Label(frame, image=self.icon, height=50, bg=CONFIG.COLORS.BACKGROUND)
        x.grid(row=1, column=1)
        y = tk.Label(frame, image=self.icon)
        y.grid(row=1, column=2)
        z = tk.Label(frame, image=self.icon)
        z.grid(row=1, column=3)
        a = tk.Label(frame, image=self.icon)
        a.grid(row=1, column=4)
        b = tk.Label(frame, image=self.icon)
        b.grid(row=1, column=5)

        gridpos += 1

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
        gridpos = DateItem(frame=frame, gridpos=gridpos, stringvar=values.date_date,
                           font=self.font_date, color=CONFIG.COLORS.DATE).gridpos
        gridpos = DateItem(frame=frame, gridpos=gridpos, stringvar=values.date_time,
                           font=self.font_date_bold, color=CONFIG.COLORS.DATE).gridpos


###############################################################################
# Weather #####################################################################
class Weather (object):
    """manages tk's root window"""
    def __init__ (self):
        self.root = tk.Tk()
        self.root.overrideredirect(1)

        self.root.resizable(width=False, height=False)
        # w = self.root.winfo_screenwidth()
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

