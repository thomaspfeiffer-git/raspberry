#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Buzzer.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2021                              #
###############################################################################
""" """


### usage ###
# nohup ./Buzzer.py 2>&1 >buzzer.log &


### useful ressources ###
# turn off screen saver:
# sudo apt-get install xscreensaver
# start xscreensaver and set screensaver off manually


import tkinter as tk
from tkinter.font import Font

import os
import subprocess
import sys
import threading
import time

sys.path.append('../libs')
from Shutdown import Shutdown
from Logging import Log



###############################################################################
###############################################################################
class Display (threading.Thread):
    """ """
    def __init__ (self):
        threading.Thread.__init__(self)
        self._running = False

    def run (self):
        self._running = True
        while self._running:
            time.sleep(0.5)

    def stop (self):
        self._running = False


###############################################################################
###############################################################################
class Sender (object):
    """ """
    def __init__ (self):
        self.filename  = "counter.txt"
        self.user      = "thomas"
        self.host      = "arverner.smtp.at"
        self.directory = "www/sonstiges/"

    def send (self, data):
        subprocess.run(["bash", "-c", f"echo \"{data}\" > {self.filename}"])
        subprocess.run(["scp", f"{self.filename}", f"{self.user}@{self.host}:{self.directory}"])


###############################################################################
###############################################################################
class Counter (threading.Thread):
    """ """
    def __init__ (self):
        threading.Thread.__init__(self)
        self.counter = 0
        self.sender = Sender()
        self._running = False

    def init_values (self, master):
        self.counter_tk = tk.StringVar(master)  # todo: improve? only one variable?

    def run (self):
        self._running = True
        while self._running:
            self.counter += 1
            self.counter_tk.set(self.counter)
            self.sender.send(self.counter)
            time.sleep(1)

    def stop (self):
        self._running = False


###############################################################################
###############################################################################
class ScreenApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.master = master

        self.font = Font(family="Arial", size=400, weight="bold")

        self.screen = tk.Frame(self.master)
        self.screen.config(bg="white", width=self.master.width,
                                       height=self.master.height)

        counter.init_values(self)
        counter.start()
        self.counter = counter.counter_tk

        self.text = tk.Label(self.screen, textvariable=self.counter,
                             foreground="red", background="white",
                             font=self.font)
        self.text.place(relx=.5, rely=.5, anchor="center")

        self.screen.grid()


###############################################################################
###############################################################################
class Screen (object):
    """  """
    def __init__ (self):
        self.root = tk.Tk()
        self.root.overrideredirect(1)
        self.root.config(cursor='none')
        self.root.resizable(width=False, height=False)

        self.root.width  = self.root.winfo_screenwidth()
        self.root.height = self.root.winfo_screenheight()
        self.root.borderwidth = 10
        self.root.geometry("{}x{}+{}+{}".format(self.root.width,
                                                self.root.height, 0, 0))
        self.root.config(bg="lightblue")
        self.app = ScreenApp(master=self.root)

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
    Log("Shutdown.")

    counter.stop()
    counter.join()

    screen.stop()
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

    counter = Counter()

    screen = Screen()
    screen.run()

# eof #

