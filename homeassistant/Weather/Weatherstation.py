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
        self.grid(row=gridpos, column=0, sticky=sticky)


class Image (tk.Label, Displayelement):
    def __init__ (self, frame, gridpos, image):
        super().__init__(frame, image=image, background=CONFIG.COLORS.BACKGROUND)
        self.gridpos = gridpos+1 
        self.grid(row=gridpos, column=0, sticky="we")


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
        self.grid(row=gridpos, column=0, sticky="we")


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
    """dedicated thread for updating the date and time fields"""
    def __init__ (self):
        threading.Thread.__init__(self)
        self.__running = False

    def init_values (self, master):  # TODO Check why master is needed
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
    """dedicated thread for updating all weather items"""
    def __init__ (self):
        threading.Thread.__init__(self)
        self.queue = SensorQueueClient_read("../config.ini")
        self.values = { "ID_{:02d}".format(id+1): None for id in range(40) }
        self.values.update({ "ID_OWM_{:02d}".format(id+1): None for id in range(30) })
        self.__running = False

    def init_values (self, master): # TODO Useage of master?
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
                for _ in range(10):
                   time.sleep(0.1)
                   if not self.__running:
                       break

    def stop (self):
        self.__running = False


###############################################################################
# WeatherApp ##################################################################
class WeatherApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.screennames = "main owm kid kb_outdoor kb_indoor wardrobe".split()
        self.master = master

        clock.init_values(self.master)
        clock.start()
        values.init_values(self.master)
        values.start()

        family = "Arial" # TODO: get from config file
        self.font_item      = Font(family=family, size=CONFIG.FONTS.SIZE_NORMAL)
        self.font_separator = Font(family=family, size=CONFIG.FONTS.SIZE_TINY)
        self.font_date      = Font(family=family, size=CONFIG.FONTS.SIZE_SMALL)
        self.font_date_bold = Font(family=family, size=CONFIG.FONTS.SIZE_SMALL, weight="bold")

        self.grid()
        self.create_screens()
        self.create_dateframe(self.master)

        self.master.bind("<Button-1>", self.next_screen())


    def next_screen (self):
        """pagination of screens with fallback to first (main) screen after
           CONFIG.TIMETOFALLBACK milliseconds
           triggered by bind("<Button-1>")"""
        screenid = 0  # ID of currently displayed screen
        reset = None

        def first_screen ():
            """switch back to first screen after 
               CONFIG.TIMETOFALLBACK milliseconds"""
            nonlocal screenid, reset

            if screenid != 0:
                self.screens[self.screennames[screenid]].grid_remove()
                screenid = 0
                self.screens[self.screennames[screenid]].grid()
            reset = None
 
        def next (event):
            """do pagination of screens and set callback to first_screen()
               after CONFIG.TIMETOFALLBACK milliseconds"""
            nonlocal screenid, reset

            if reset is not None:
                self.master.after_cancel(reset)
                reset = None

            self.screens[self.screennames[screenid]].grid_remove()
            screenid += 1
            if screenid >= len(self.screennames): 
                screenid = 0
            self.screens[self.screennames[screenid]].grid()

            # switch to first screen after CONFIG.TIMETOFALLBACK milliseconds
            reset = self.master.after(CONFIG.TIMETOFALLBACK, first_screen)

        return next


    def create_screens (self):
        self.screens = OrderedDict()
        for screen in self.screennames:
            self.screens[screen] = tk.Frame(self)
            self.screens[screen].config(bd=self.master.borderwidth, 
                                        bg=CONFIG.COLORS.BACKGROUND, 
                                        width=self.master.width, height=410)
            self.screens[screen].grid_propagate(0)    
            self.screens[screen].grid_columnconfigure(0, minsize=self.master.width - \
                                                         2*self.master.borderwidth)
            getattr(self, "create_screen_{}".format(screen))() # call create_screen_X()

        self.screens['main'].grid()


    def create_dateframe (self, master):
        self.dateframe = tk.Frame(master)
        self.dateframe.config(bd=self.master.borderwidth, 
                              bg=CONFIG.COLORS.BACKGROUND, 
                              width=self.master.width, height=70)
        self.dateframe.grid_propagate(0)
        self.dateframe.grid_columnconfigure(0, minsize=self.master.width - \
                                                       2*self.master.borderwidth)
        self.dateframe.grid()

        gridpos = 0
        gridpos = Separator(frame=self.dateframe, gridpos=gridpos).gridpos
        for d in [clock.date_date, clock.date_time]:
            gridpos = DateItem(frame=self.dateframe, gridpos=gridpos, 
                               stringvar=d, font=self.font_date, 
                               color=CONFIG.COLORS.DATE).gridpos


    def drawWeatherSection (self, frame, title, itemlist, color, gridpos):
        gridpos = Separator(frame=frame, gridpos=gridpos, text=title, 
                            font=self.font_separator).gridpos
        for item in itemlist:
            gridpos = WeatherItem(frame=frame, gridpos=gridpos, 
                                  stringvar=values.values[item],
                                  font=self.font_item, color=color).gridpos
        return gridpos


    def drawPicture (self, frame, picture, id_, zoom, gridpos):
        picture = PIL.Image.open(picture)
        w, h = picture.size
        w = int(w*zoom)
        h = int(h*zoom)
        picture = picture.resize((w, h), PIL.Image.ANTIALIAS)

        # image needs to stored garbage collector save, otherwise the 
        # image would be deleted by the garbage collector and therefore
        # it would not be displayed.
        attrname = "picture_{}".format(id_) 
        setattr(self, attrname, PIL.ImageTk.PhotoImage(picture))
        gridpos = Image(frame=frame, gridpos=gridpos, 
                        image=getattr(self,attrname)).gridpos
        return gridpos
        

    def create_screen_main (self):
        frame = self.screens['main']
        gridpos = 0

        """
        icon = PIL.Image.open("../Resources/ico_sunny.png")
        icon = icon.resize((40, 40),  PIL.Image.ANTIALIAS)
        self.icon = PIL.ImageTk.PhotoImage(icon)

        icons = [i for i in range(5)]
        for i in range(len(icons)):
            icons[i] = tk.Label(frame, image=self.icon, 
                                height=50, bg=CONFIG.COLORS.BACKGROUND)
            icons[i].grid(row=gridpos, column=i+1)
        gridpos += 1
        """

        gridpos = self.drawWeatherSection(frame=frame, title="Wohnzimmer:",
                                          itemlist=['ID_01', 'ID_02'],
                                          color=CONFIG.COLORS.INDOOR,
                                          gridpos=gridpos)
        gridpos = self.drawWeatherSection(frame=frame, title="Draußen:",
                                          itemlist=['ID_12', 'ID_04', 'ID_05'],
                                          color=CONFIG.COLORS.INDOOR,
                                          gridpos=gridpos)


    def create_screen_owm (self):
        frame = self.screens['owm']
        gridpos = 0

        gridpos = self.drawWeatherSection(frame=frame, title="Wettervorhersage aktuell:",
                                          itemlist=['ID_OWM_01', 'ID_OWM_02'],
                                          color=CONFIG.COLORS.FORECAST,
                                          gridpos=gridpos)


    def create_screen_kid (self):
        frame = self.screens['kid']
        gridpos = 0

        gridpos = self.drawWeatherSection(frame=frame, title="Kinderzimmer:",
                                          itemlist=['ID_06', 'ID_07'],
                                          color=CONFIG.COLORS.KIDSROOM,
                                          gridpos=gridpos)
        gridpos = self.drawPicture(frame=frame, picture=CONFIG.IMAGES.PIC_KIDSROOM,
                                   id_='kid', zoom=0.9, gridpos=gridpos)


    def create_screen_kb_outdoor (self):
        frame = self.screens['kb_outdoor']
        gridpos = 0

        gridpos = self.drawWeatherSection(frame=frame, title="Kollerberg (außen):",
                                          itemlist=['ID_24', 'ID_25', 'ID_23'],
                                          color=CONFIG.COLORS.COTTAGE,
                                          gridpos=gridpos)
        gridpos = self.drawPicture(frame=frame, picture=CONFIG.IMAGES.PIC_COTTAGE,
                                   id_='kb', zoom=0.8, gridpos=gridpos)


    def create_screen_kb_indoor (self):
        frame = self.screens['kb_indoor']
        gridpos = 0

        gridpos = self.drawWeatherSection(frame=frame, title="Kollerberg (innen):",
                                          itemlist=['ID_21', 'ID_22'],
                                          color=CONFIG.COLORS.COTTAGE,
                                          gridpos=gridpos)
        gridpos = self.drawWeatherSection(frame=frame, title="Kollerberg (Keller):",
                                          itemlist=['ID_26', 'ID_27'],
                                          color=CONFIG.COLORS.COTTAGE,
                                          gridpos=gridpos)


    def create_screen_wardrobe (self):
        frame = self.screens['wardrobe']
        gridpos = 0

        gridpos = self.drawWeatherSection(frame=frame, title="Schlafzimmerkasten:",
                                          itemlist=['ID_31', 'ID_32', 'ID_33'],
                                          color=CONFIG.COLORS.WARDROBE,
                                          gridpos=gridpos)
        gridpos = self.drawWeatherSection(frame=frame, title="Misc:",
                                          itemlist=['ID_03', 'ID_13'],
                                          color=CONFIG.COLORS.MISC,
                                          gridpos=gridpos)


###############################################################################
# Weather #####################################################################
class Weather (object):
    """manages tk's root window"""
    def __init__ (self):
        self.root = tk.Tk()
        self.root.overrideredirect(1)
        self.root.config(cursor='none')

        self.root.resizable(width=False, height=False)
        # w = self.root.winfo_screenwidth() # TODO Get coordinates and dimension from config file
        w = 280 # TODO beautify code
        h = self.root.winfo_screenheight()
        self.root.width = 280
        self.root.height = self.root.winfo_screenheight()
        self.root.borderwidth = 10
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

# eof #

