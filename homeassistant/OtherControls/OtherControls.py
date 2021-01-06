#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# OtherControls.py                                                            #
# (c) https://github.com/thomaspfeiffer-git 2017, 2021                        #
###############################################################################
"""Part of the homeautomation project: switch lights on/off in anteroom
   and control radio application"""

### usage ###
# nohup ./OtherControls.py &


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
class Control (object):
    def __init__ (self):
        pass

    @staticmethod
    def call_url (request):
        Log(f"Request: {request}")
        try:
            urlopen(request, timeout=2)
        except (HTTPError, URLError):
            Log("HTTPError, URLError: {0[0]} {0[1]}".format(sys.exc_info()))
        except socket.timeout:
            Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info()))

    def toggle_radio (self, on):
        if Touchevent.event():   # brightness control
            Sound.play(CONFIG.CLICK_SOUND)

            request = CONFIG.RADIO.BASE_URL
            request += "showapp" if on else "radiooff"
            self.call_url(request)

    def toggle_light (self):
        if Touchevent.event():   # brightness control
            Sound.play(CONFIG.CLICK_SOUND)
            self.call_url(CONFIG.URL_ANTEROOM_CONTROL)


###############################################################################
# OtherControlsApp ############################################################
class OtherControlsApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.master = master
        self.pack()

        self.create_elements()

    def create_elements (self):
        self.frame  = tk.Frame(self.master, bg=CONFIG.COLORS.BACKGROUND,
                               width=CONFIG.COORDINATES.WIDTH,
                               height=CONFIG.COORDINATES.HEIGHT)
        self.frame.pack_propagate(0)
        self.frame.pack()

        self.style = ttk.Style()
        self.style.configure("Radio.TButton",
                             font=(CONFIG.FONTS.FAMILY, CONFIG.FONTS.SIZE_NORMAL),
                             width=5, background=CONFIG.COLORS.BUTTON_RADIO)
        self.style.map("Radio.TButton", background=[('active', CONFIG.COLORS.BUTTON_RADIO)],
                                           relief=[('pressed', 'groove'),
                                                   ('!pressed', 'ridge')])
        font_off = Font(family=CONFIG.FONTS.FAMILY, size=CONFIG.FONTS.SIZE_NORMAL, overstrike=True)
        self.style.configure("Off.Radio.TButton",
                             font=font_off,
                             width=5, background=CONFIG.COLORS.BUTTON_RADIO)
        self.style.map("Off.Radio.TButton", background=[('active', CONFIG.COLORS.BUTTON_RADIO)],
                                           relief=[('pressed', 'groove'),
                                                   ('!pressed', 'ridge')])
        self.style.configure("Anteroom.TButton",
                             font=(CONFIG.FONTS.FAMILY, CONFIG.FONTS.SIZE_NORMAL),
                             width=5, background=CONFIG.COLORS.BUTTON_ANTEROOM)
        self.style.map("Anteroom.TButton", background=[('active', CONFIG.COLORS.BUTTON_ANTEROOM)],
                                           relief=[('pressed', 'groove'),
                                                   ('!pressed', 'ridge')])

        self.button_radio_on = ttk.Button(self.frame, text="Radio", style="Radio.TButton", command=lambda: control.toggle_radio(on=True))
        self.button_radio_off = ttk.Button(self.frame, text="Radio", style="Off.Radio.TButton", command=lambda: control.toggle_radio(on=False))
        self.button_radio_on.pack(padx=5, pady=5)
        self.button_radio_off.pack(padx=5, pady=5)

        self.button_anteroom = ttk.Button(self.frame, text="Licht", style="Anteroom.TButton", command=control.toggle_light)
        self.button_anteroom.pack(padx=5, pady=5)

        # brightness control:
        # brightness control runs in a dedicated application (see ../Brightness/).
        # each touch event is first sent to the brightness control
        # (Touchevent.event()):
        # - brightness is low:  set brightness to max and return False
        # - brightness is high: return True
        self.frame.bind("<Button-1>", Touchevent.event) # brightness control


###############################################################################
# Anteroom ####################################################################
class OtherControls (object):
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
        self.app = OtherControlsApp(master=self.root)

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
        self.root.quit()


###############################################################################
# shutdown_application ########################################################
def shutdown_application ():
    """called on shutdown; stops all threads"""
    Log("Stopping application")
    other_controls.stop()
    Log("Application stopped")
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
    other_controls = OtherControls()
    other_controls.run()

# eof #

