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

sys.path.append('../../libs')
from Shutdown import Shutdown
from Logging import Log



class Countdown (object):
    def __init__ (self):
        self.__counter = 0

    @property
    def counter (self, value): 
        return self.__counter 

    @counter.setter
    def counter (self):
        self.__counter = value
 
    def __str__ (self):
        return "{}".format(self.counter)
 

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
        self.buttons = OrderedDict({ 'p5': ttk.Button(self.frame, text="+5", style="Timer.TButton"),
                         'p1': ttk.Button(self.frame, text="+1", style="Timer.TButton"),
                         'm1': ttk.Button(self.frame, text="-1", style="Timer.TButton"),
                         'm5': ttk.Button(self.frame, text="-5", style="Timer.TButton"),
                         'reset': ttk.Button(self.frame, text="Reset", style="Timer.TButton")
                       })
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

        # self.buttonframe = tk.Frame(self, bg="red", width=110, height=300)
        # self.buttonframe.pack_propagate(0) 
        # self.buttonframe.pack()

        # self.buttonstyle = ttk.Style()
        # self.buttonstyle.configure("Timer.TButton", font=("Arial", 20, "bold"), 
        #                            width=5, background="DodgerBlue")

        # self.button_p5 = ttk.Button(self.buttonframe, text="+5", style="Timer.TButton")
        # self.button_p1 = ttk.Button(self.buttonframe, text="+1", style="Timer.TButton")
        # self.button_m1 = ttk.Button(self.buttonframe, text="–1", style="Timer.TButton")
        # self.button_m5 = ttk.Button(self.buttonframe, text="–5", style="Timer.TButton")
        # self.button_reset = ttk.Button(self.buttonframe, text="Reset", style="Timer.TButton")
        # self.button_p5.pack(padx=5, pady=5)
        # self.button_p1.pack(padx=5, pady=5)
        # self.button_m1.pack(padx=5, pady=5)
        # self.button_m5.pack(padx=5, pady=5)
        # self.button_reset.pack(padx=5, pady=5)



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

