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

import os
import sys

sys.path.append('../../libs')
from Shutdown import Shutdown
from Logging import Log


###############################################################################
# TimerApp ####################################################################
class TimerApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.master = master
        self.pack()

        self.buttonframe = tk.Frame(self, bg="red")
        self.buttonframe.pack()

        self.buttonstyle = ttk.Style()
        self.buttonstyle.configure("Timer.TButton", font=("Arial", 20, "bold"), 
                                   width=5, background="DodgerBlue")

        self.button_p5 = ttk.Button(self.buttonframe, text="+5", style="Timer.TButton")
        self.button_p1 = ttk.Button(self.buttonframe, text="+1", style="Timer.TButton")
        self.button_m1 = ttk.Button(self.buttonframe, text="–1", style="Timer.TButton")
        self.button_m5 = ttk.Button(self.buttonframe, text="–5", style="Timer.TButton")
        self.button_p5.pack()
        self.button_p1.pack()
        self.button_m1.pack()
        self.button_m5.pack()



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
