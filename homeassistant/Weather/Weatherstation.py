#!/usr/bin/python3 -u
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


import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font
import PIL.Image
import PIL.ImageTk

from collections import OrderedDict
from datetime import datetime
import json
import os
import sys
import threading
import time
from urllib.error import HTTPError, URLError 
from urllib.request import urlopen

sys.path.append('../../libs')
from SensorQueue2 import SensorQueueClient_read
from Shutdown import Shutdown

from Config import CONFIG
from Constants import CONSTANTS


def Log (logstr):
    """improved log output"""
    print("{}: {}".format(datetime.now().strftime("%Y%m%d %H:%M:%S"), logstr))


###############################################################################
# Basic display elements ######################################################
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
        # TODO: type safety: image
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
    def __init__ (self, frame, gridpos, text=None, vartext=None, font=None):
        super().__init__(frame, gridpos=gridpos, text=text, stringvar=vartext,
                         anchor="w", sticky="we", font=font, color=CONFIG.COLORS.SEP)


class SeparatorLine (ttk.Separator, Displayelement):
    """prints separator line"""
    def __init__ (self, frame, gridpos):
        super().__init__(frame, orient="horizontal")
        self.gridpos = gridpos+1
        self.grid(row=gridpos, column=0, sticky="we")


class Separator (Displayelement): 
    """prints a separator which consists of a line and some text"""
    def __init__ (self, frame, gridpos, text=None, vartext=None, font=None):
        self.gridpos = SeparatorLine(frame=frame, gridpos=gridpos).gridpos
        if text is not None or vartext is not None:
            self.gridpos = SeparatorText(frame=frame, gridpos=self.gridpos,
                                         text=text, vartext=vartext, 
                                         font=font).gridpos


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
        if sensorvalue is not None:
            return sensorvalue.value
        else:
            return "(n/a)"

    def calculate_local_values (self):
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


###############################################################################
# Pagination ##################################################################
class Pagination (object):
    """pagination of screens with fallback to first (main) screen after
       CONFIG.TIMETOFALLBACK milliseconds
       triggered by bind("<Button-1>")"""
    def __init__ (self, master, screens, screennames):
        self.master  = master
        self.screens = screens
        self.screennames = screennames
        self.screenid = 0
        self.reset    = None
     
    def turn_page (self):
        """send the touch event to the brightness controller.
           if brightness was not at full level, the brightness
           controller sets brightness to full. in this case, no
           pagination shall be done."""
        try:
            with urlopen(CONFIG.URL_BRIGHTNESS_CONTROL) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError):
            Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
        else:
            return data['FullBrightness']
        return True
 
    def first_screen (self):
        """switch back to first screen after 
           CONFIG.TIMETOFALLBACK milliseconds"""
        if self.screenid != 0:
            self.screens[self.screennames[self.screenid]].grid_remove()
            self.screenid = 0
            self.screens[self.screennames[self.screenid]].grid()
        self.reset = None

    def next_screen (self, event):
        """do pagination of screens and set callback to first_screen()
           after CONFIG.TIMETOFALLBACK milliseconds"""

        if not self.turn_page():
            return

        if self.reset is not None:
            self.master.after_cancel(self.reset)
            self.reset = None

        self.screens[self.screennames[self.screenid]].grid_remove()
        self.screenid += 1
        if self.screenid >= len(self.screennames): 
            self.screenid = 0
        self.screens[self.screennames[self.screenid]].grid()

        self.reset = self.master.after(CONFIG.TIMETOFALLBACK, self.first_screen)


###############################################################################
# WeatherApp ##################################################################
class WeatherApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.screennames = "main owm kid kb_outdoor kb_indoor wardrobe".split()
        self.master = master

        clock.init_values()
        values.init_values()

        self.init_fonts()

        self.grid()
        self.create_screens()
        self.create_dateframe(self.master)

        self.pagination = Pagination(self.master, self.screens, self.screennames)
        self.master.bind("<Button-1>", self.pagination.next_screen)

        clock.start()
        values.start()


    def init_fonts (self):
        family = CONFIG.FONTS.FAMILY
        self.font_item      = Font(family=family, size=CONFIG.FONTS.SIZE_NORMAL)
        self.font_forecast  = Font(family=family, size=CONFIG.FONTS.SIZE_FORECAST)
        self.font_separator = Font(family=family, size=CONFIG.FONTS.SIZE_TINY)
        self.font_date      = Font(family=family, size=CONFIG.FONTS.SIZE_SMALL)
        self.font_date_bold = Font(family=family, size=CONFIG.FONTS.SIZE_SMALL, weight="bold")


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


    def drawForecastSection (self, frame, vartitle, itemlist, gridpos):
        gridpos = Separator(frame=frame, gridpos=gridpos, 
                            vartext=values.values[vartitle],
                            font=self.font_separator).gridpos
        for item in itemlist:
            gridpos = WeatherItem(frame=frame, gridpos=gridpos, 
                                  stringvar=values.values[item],
                                  font=self.font_forecast, 
                                  color=CONFIG.COLORS.FORECAST).gridpos
        return gridpos


    def drawPicture (self, frame, picture, id_, zoom, gridpos):
        picture = PIL.Image.open(picture)
        w, h = map(lambda x: int(x*zoom), picture.size)
        picture = picture.resize((w, h), PIL.Image.ANTIALIAS)

        # image needs to be stored garbage collector save, otherwise the 
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

        gridpos = self.drawForecastSection(frame=frame, vartitle='ID_LC_01',
                                           itemlist=['ID_OWM_05', 'ID_LC_02', 'ID_LC_03'],
                                           gridpos=gridpos)
        gridpos = self.drawForecastSection(frame=frame, vartitle='ID_LC_11',
                                           itemlist=['ID_OWM_15', 'ID_LC_12', 'ID_LC_13'],
                                           gridpos=gridpos)
        gridpos = self.drawForecastSection(frame=frame, vartitle='ID_LC_21',
                                           itemlist=['ID_OWM_25', 'ID_LC_22', 'ID_LC_23'],
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

        self.root.width  = CONFIG.COORDINATES.WIDTH
        self.root.height = CONFIG.COORDINATES.HEIGHT
        self.root.borderwidth = 10
        self.root.geometry("{}x{}+{}+{}".format(self.root.width, 
                                                self.root.height,
                                                CONFIG.COORDINATES.XPOS, 
                                                CONFIG.COORDINATES.XPOS))
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
    Log("shutdown_application()")
    clock.stop()
    clock.join()
    print("after clock.join()")
    values.stop()
    values.join()
    print("after values.join()")
    weather.stop()
    print("after weather.stop()")
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    try:
        os.environ["DISPLAY"]
    except KeyError:
        Log("$DISPLAY not set, using default :0.0")
        os.environ["DISPLAY"] = ":0.0"
    shutdown = Shutdown(shutdown_func=shutdown_application)

    values = Values()
    clock  = Clock()

    weather = Weather()
    weather.run()

# eof #

