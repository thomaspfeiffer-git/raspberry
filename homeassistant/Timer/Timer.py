#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Timer.py                                                                    #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
###############################################################################
"""
"""

### usage ###
# nohup ./Timer.py &


import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font

from collections import OrderedDict
import os
import sys
import time

sys.path.append('../../libs')
from Shutdown import Shutdown
from Logging import Log


class Countdown (object):
    def __init__ (self):
        self.reset()

    @property
    def counter (self):
        return self.__counter 

    @counter.setter
    def counter (self, value): 
        self.__counter = value
        print("counter: {}".format(self.counter))

    def alter (self, value):
        self.counter += value

    def reset (self, value=0):
        self.counter = value
 
    def __str__ (self):
        return "{}".format(self.counter)

    def run (self):
        self.__running = True
        while self.__running:
            time.sleep(0.1)
            # reduce counter every second
            ## control.timedisplay == tk.StringVar()
            # control.timedisplay.set("{}".format(self.counter))

    def stop (self):
        self.__running = False

 
class Control (object):
    def __init__ (self, frame, counter):
        self.master = frame
        self.frame  = tk.Frame(self.master, bg="red", width=110, height=300)
        self.frame.pack_propagate(0)
        self.frame.pack()
 
        self.counter = counter
 
        self.style = ttk.Style()
        self.style.configure("Timer.TButton", font=("Arial", 20, "bold"),
                             width=5, background="DodgerBlue")
        self.buttons = OrderedDict()
        self.buttons.update({'p5': ttk.Button(self.frame, text="+5", style="Timer.TButton", command = lambda: self.counter.alter(5*60))})
        self.buttons.update({'p1': ttk.Button(self.frame, text="+1", style="Timer.TButton", command = lambda: self.counter.alter(1*60))})
        self.buttons.update({'m1': ttk.Button(self.frame, text="-1", style="Timer.TButton", command = lambda: self.counter.alter(-1*60))})
        self.buttons.update({'m5': ttk.Button(self.frame, text="-5", style="Timer.TButton", command = lambda: self.counter.alter(-5*60))})
        self.buttons.update({'reset': ttk.Button(self.frame, text="Reset", style="Timer.TButton", command = self.counter.reset)})
        for btn in self.buttons.values():
            btn.pack(padx=5, pady=5)


###############################################################################
# TimerApp ####################################################################
class TimerApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.master = master
        self.pack()

        self.counter = Countdown()
        self.control = Control(self, self.counter)


###############################################################################
# Timer #######################################################################
class Timer (object):
    def __init__ (self):
        self.root = tk.Tk()

        self.root.overrideredirect(1)
        self.root.config(cursor='none')
        self.root.resizable(width=False, height=False)

        self.root.width  = 300   # TODO: config file
        self.root.height = 480
        self.root.borderwidth = 10

        self.root.geometry("300x480+100+0")   # TODO: config file
        self.root.config(bg="yellow")
        self.app = TimerApp(master=self.root)
        
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

    timer.stop()
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

    timer = Timer()
    timer.run()

# eof #

