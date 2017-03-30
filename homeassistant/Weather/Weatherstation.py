#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# Weatherstation.py                                                           #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
###############################################################################
"""Weatherstation: collects various data from sensors in our flat and garden
   and displays them on a Touch Screen Display."""

### usage ###
# export DISPLAY=:0.0
# ./Weatherstation.py


### useful ressources ###
# turn off screen saver:
# http://www.etcwiki.org/wiki/Disable_screensaver_and_screen_blanking_Raspberry_Pi
# http://raspberrypi.stackexchange.com/questions/752/how-do-i-prevent-the-screen-from-going-blank




import tkinter as tk
# import threading
import sys


sys.path.append('../../libs')
from SensorQueue2 import SensorQueueClient_read
from Shutdown import Shutdown

from Config import CONFIG


###############################################################################
# WeatherApp ##################################################################
class WeatherApp (tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.grid()

        temp_indoor = tk.StringVar()
        self.temp_indoor = tk.Label(self,
                                    font="{} {}".format(CONFIG.FONT, CONFIG.FONTSIZE),
                                    justify="left",
                                    anchor="w",
                                    fg=CONFIG.COLORS.INDOOR)
        # self.temp_indoor.pack(side="top")
        self.temp_indoor.grid(row=1, column=1, sticky="w")
        self.temp_indoor['textvariable'] = temp_indoor
        temp_indoor.set("23.7 °C")

        humi_indoor = tk.StringVar()
        self.humi_indoor = tk.Label(self,
                                    font="{} {}".format(CONFIG.FONT, CONFIG.FONTSIZE),
                                    justify="left",
                                    anchor="w",
                                    fg=CONFIG.COLORS.INDOOR)
        # self.humi_indoor.pack(side="top")
        self.humi_indoor.grid(row=2, column=1, sticky="w")
        self.humi_indoor['textvariable'] = humi_indoor
        humi_indoor.set("1013 hPa")

    def say_hi(self):
        print("hi there, everyone!")


###############################################################################
# Weather #####################################################################
class Weather (object):
    """manages tk's root window"""
    def __init__ (self):
        self.root = tk.Tk()
        self.root.overrideredirect(1)

        self.root.resizable(width=False, height=False)
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        w = self.width // 2
        h = self.height
        self.root.geometry("{}x{}+{}+{}".format(w,h,0,0))

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

