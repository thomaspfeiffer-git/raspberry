#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Anteroom.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
###############################################################################
"""Part of the homeautomation project: switch lights on/off in anteroom."""

### usage ###
# nohup ./Anteroom.py &


import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font

import os
import socket
import sys
import threading
import time
from urllib.error import HTTPError, URLError 
from urllib.request import urlopen


sys.path.append('../../libs')
from Logging import Log
from Shutdown import Shutdown

sys.path.append('../libraries')
from touchevent import Touchevent
from sound import Sound

from config import CONFIG


###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    """creates all display elements and corresponding callback methods
       for the business logic (increase and decrease timer; alarm).
    """
    def __init__ (self):
        self._running = False
        threading.Thread.__init__(self)

    def create_elements (self, frame):
        self.master = frame
        self.frame  = tk.Frame(self.master, bg=CONFIG.COLORS.BACKGROUND,
                               width=CONFIG.COORDINATES.WIDTH, 
                               height=CONFIG.COORDINATES.HEIGHT)
        self.frame.pack_propagate(0)
        self.frame.pack()
 
        self.style = ttk.Style()
        self.style.configure("Anteroom.TButton", 
                             font=(CONFIG.FONTS.FAMILY, CONFIG.FONTS.SIZE_NORMAL),
                             width=5, background=CONFIG.COLORS.BUTTON)
        self.style.map("Anteroom.TButton", background=[('active', CONFIG.COLORS.BUTTON)],
                                           relief=[('pressed', 'groove'),
                                                   ('!pressed', 'ridge')])
        self.button = ttk.Button(self.frame, text="Licht", style="Anteroom.TButton", command = self.toggle)
        self.button.pack(padx=5, pady=5)

        # brightness control:
        # brightness control runs in a dedicated application (see ../Brightness/).
        # each touch event is first sent to the brightness control 
        # (Touchevent.event()):
        # - brightness is low:  set brightness to max and return False
        # - brightness is high: return True
        self.frame.bind("<Button-1>", Touchevent.event) # brightness control

    def toggle (self):
        if Touchevent.event():   # brightness control
            Sound.play(CONFIG.CLICK_SOUND)
            try:
                urlopen(CONFIG.URL_ANTEROOM_CONTROL, timeout=2)
            except (HTTPError, URLError):
                Log("HTTPError, URLError: {0[0]} {0[1]}".format(sys.exc_info()))
            except socket.timeout:
                Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info()))

    def run (self):
        self._running = True
        while self._running:
            time.sleep(0.05)

    def stop (self):
        self._running = False


###############################################################################
# AnteroomApp #################################################################
class AnteroomApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.master = master
        self.pack()

        control.create_elements(self)
        control.start()


###############################################################################
# Anteroom ####################################################################
class Anteroom (object):
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
        self.app = AnteroomApp(master=self.root)

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

    anteroom.stop()

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

    control = Control()

    anteroom = Anteroom()
    anteroom.run()

# eof #

