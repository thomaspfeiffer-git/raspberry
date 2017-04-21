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
from datetime import datetime
import os
import sys
import threading
import time

sys.path.append('../../libs')
from Shutdown import Shutdown
from Logging import Log

from config import CONFIG


###############################################################################
# Countdown ###################################################################
class Countdown (threading.Thread):
    def __init__ (self, value=0):
        self.__running = False
        threading.Thread.__init__(self)
        self.__lock = threading.RLock()
        self.reset(value)

    @property
    def counter (self):
        return self.__counter 

    @counter.setter
    def counter (self, value):
        with self.__lock:
            self.__counter = value
            if self.__counter < 0:
                self.__counter = 0

    def alter (self, value):
        with self.__lock:
            self.counter += value

    def reset (self, value=0):
        self.counter = value
 
    def run (self):
        self.__running = True
        now = datetime.now().timestamp()
        while self.__running:
            time.sleep(0.1)
            if datetime.now().timestamp() > now + 1.0:
                self.alter(-1)
                now = datetime.now().timestamp() 

    def stop (self):
        print("Countdown.stop()")
        self.__running = False

 
###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    def __init__ (self):
        self.__running = False
        threading.Thread.__init__(self)

    def create_elements (self, frame):
        self.master = frame
        self.frame  = tk.Frame(self.master, bg=CONFIG.COLORS.BACKGROUND,
                               width=CONFIG.COORDINATES.WIDTH, 
                               height=CONFIG.COORDINATES.HEIGHT)
        self.frame.pack_propagate(0)
        self.frame.pack()
 
        self.style = ttk.Style()
        self.style.configure("Timer.TButton", 
                             font=(CONFIG.FONTS.FAMILY, CONFIG.FONTS.SIZE_NORMAL, "bold"),
                             width=5, background=CONFIG.COLORS.BUTTON)
        self.style.map("Timer.TButton", background=[('active', CONFIG.COLORS.BUTTON)])

        self.buttons = OrderedDict()
        self.buttons.update({'p5': ttk.Button(self.frame, text="+5", style="Timer.TButton", command = lambda: countdown.alter(5*60))})
        self.buttons.update({'p1': ttk.Button(self.frame, text="+1", style="Timer.TButton", command = lambda: countdown.alter(1*60))})
        self.buttons.update({'m1': ttk.Button(self.frame, text="-1", style="Timer.TButton", command = lambda: countdown.alter(-1*60))})
        self.buttons.update({'m5': ttk.Button(self.frame, text="-5", style="Timer.TButton", command = lambda: countdown.alter(-5*60))})
        self.buttons.update({'reset': ttk.Button(self.frame, text="Reset", style="Timer.TButton", command = self.reset)})
        for btn in self.buttons.values():
            btn.pack(padx=5, pady=5)

        self.timer = tk.StringVar()
        self.timerdisplay = ttk.Label(self.frame, textvariable=self.timer, style="Timer.TButton")
        self.timerdisplay.pack(padx=5, pady=5)

    def reset (self):
        """resets the timer and switches alarm off"""
        countdown.reset()
        # alarm.off()

    def run (self):
        self.__running = True
        lastvalue = 0
        while self.__running:
            time.sleep(0.1)
            value = countdown.counter
            if value != 0:
                self.timer.set("{:d}:{:02d}".format(value // 60, value % 60))
            if lastvalue != 0 and value == 0:
                self.timer.set("Alarm")  # TODO: what if self.reset()?
            lastvalue = value

    def stop (self):
        print("Control.stop()")
        self.__running = False


###############################################################################
# TimerApp ####################################################################
class TimerApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.master = master
        self.pack()

        control.create_elements(self)
        control.start()


###############################################################################
# Timer #######################################################################
class Timer (object):
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
                                                CONFIG.COORDINATES.YPOS))
        self.root.config(bg=CONFIG.COLORS.BACKGROUND)
        self.app = TimerApp(master=self.root)
        
    def poll (self):
        """polling needed for ctrl-c"""
        self.root.pollid = self.root.after(50, self.poll)

    def run (self):
        """start polling and run application"""
        self.root.pollid = self.root.after(50, self.poll)
        self.app.mainloop()

    def stop (self):
        """stops application, called on shutdown"""
        self.root.after_cancel(self.root.pollid)
        self.root.destroy()
        self.root.quit() # TODO: check usage of destroy() and quit()


###############################################################################
# shutdown_application ########################################################
def shutdown_application ():
    """called on shutdown; stops all threads"""
    Log("shutdown_application()")

    control.stop()
    control.join()
    countdown.stop()
    countdown.join()

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

    countdown = Countdown()
    countdown.start()

    control = Control()

    timer = Timer()
    timer.run()

# eof #

