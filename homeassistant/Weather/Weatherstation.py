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
# start xscreensaver and set screensaver off manually
#
# Packages you might install
# sudo apt-get install python3-pil.imagetk


import tkinter as tk
from tkinter.font import Font
import PIL.Image
import PIL.ImageTk

from collections import OrderedDict
from datetime import datetime
import os
import sys
import time

sys.path.append('../../libs')
from Shutdown import Shutdown
from Logging import Log

from config import CONFIG
from constants import CONSTANTS
from displaybasics import WeatherItem, DateItem, Separator, Image
from pagination import Pagination
from refreshvalues import Clock, Values


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
                                          color=CONFIG.COLORS.OUTDOOR,
                                          gridpos=gridpos)
        gridpos = self.drawWeatherSection(frame=frame, title="Helligkeit Küche",
                                          itemlist=['ID_09'],
                                          color=CONFIG.COLORS.BRIGHTNESSKITCHEN,
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

