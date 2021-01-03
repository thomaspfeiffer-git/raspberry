#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Radio.py                                                                    #
# (c) https://github.com/thomaspfeiffer-git 2021                              #
###############################################################################
"""
"""

### usage ###
# ./Radio.py 2>&1 > radio.log &


# Packages you might install
# sudo apt-get install python3-pil.imagetk


import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font

from collections import OrderedDict
import os
import sys

sys.path.append('../../libs')
from Shutdown import Shutdown
from Logging import Log

sys.path.append('../libraries')
from touchevent import Touchevent

from config import CONFIG


station_name = "name"
station_url  = "url"
Stations = OrderedDict()
Stations.update({ 's1': { station_name: "88.6", station_url: "https://radio886.fluidstream.eu/886_live.mp3?FLID=7" } })
Stations.update({ 's2': { station_name: "Ö3", station_url: "https://orf-live.ors-shoutcast.at/oe3-q2a" } })
Stations.update({ 's3': { station_name: "The Sound of New York City", station_url: "http://ic2377.c900.fast-serv.com/tsonyc.mp3" } })
Stations.update({ 's4': { station_name: "BBC Radio 2", station_url: "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio2_mf_q" } })


###############################################################################
# RadioApp ####################################################################
class RadioApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.master = master
        self.frame  = tk.Frame(self.master, bg=CONFIG.COLORS.BACKGROUND,
                               width=CONFIG.COORDINATES.WIDTH,
                               height=CONFIG.COORDINATES.HEIGHT)
        self.frame.pack_propagate(0)
        self.frame.pack()

        # brightness control:
        # brightness control runs in a dedicated application (see ../Brightness/).
        # each touch event is first sent to the brightness control
        # (Touchevent.event()):
        # - brightness is low:  set brightness to max and return False
        # - brightness is high: return True
        self.master.bind("<Button-1>", Touchevent.event) # brightness control
        self.create_tk_elements()

    def play (self, url):
        Log(f"Playing {url}")

    def create_tk_elements (self):
        self.style = ttk.Style()
        self.style.configure("Radio.TButton",
                             font=(CONFIG.FONTS.FAMILY, CONFIG.FONTS.SIZE_NORMAL),
                             width=25, background=CONFIG.COLORS.BUTTON)
        self.style.map("Radio.TButton", background=[('active', CONFIG.COLORS.BUTTON)],
                                        relief=[('pressed', 'groove'),
                                                ('!pressed', 'ridge')])

        self.buttons = OrderedDict()
        for station in Stations:
            url = Stations[station][station_url]
            self.buttons.update({station: ttk.Button(self.frame, text=Stations[station][station_name],
                                                     style="Radio.TButton",
                                                     command = lambda u=url: self.play(u))})
        for btn in self.buttons.values():
            btn.pack(padx=5, pady=5)





###############################################################################
# Radio #######################################################################
class Radio (object):
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
        self.app = RadioApp(master=self.root)

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
    Log("shutdown_application()")

    radio.stop()
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

    radio = Radio()
    radio.run()

# eof #

