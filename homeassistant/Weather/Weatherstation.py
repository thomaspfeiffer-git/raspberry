#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# Weatherstation.py                                                           #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
###############################################################################
"""Weatherstation: collects various data from sensors in our flat and garden
   and displays them on a Touch Screen Display."""


# export DISPLAY=:0.0
# ./Weatherstation.py


import tkinter as tk
# import threading
import sys


sys.path.append('../../libs')
from SensorQueue2 import SensorQueueClient_read
from Shutdown import Shutdown


###############################################################################
# WeatherApp ##################################################################
class WeatherApp (tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=shutdown_application)
        self.quit.pack(side="bottom")

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

