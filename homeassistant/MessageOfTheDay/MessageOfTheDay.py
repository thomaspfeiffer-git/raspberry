#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# MessageOfTheDay.py                                                          #
# (c) https://github.com/thomaspfeiffer-git 2017, 2023                        #
###############################################################################
"""
"""

### usage ###
# nohup ./MessageOfTheDay.py &


# Packages you might install
# sudo apt-get install python3-pil.imagetk


import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font
import PIL.Image
import PIL.ImageTk

import os
import sys

sys.path.append('../../libs')
from Shutdown import Shutdown
from Logging import Log

sys.path.append('../libraries')
from touchevent import Touchevent

sys.path.append('../Weatherstation')
from refreshvalues import Clock
from displaybasics import DateItem


from config import CONFIG


# message_of_the_day = "Frohe Ostern!"
message_of_the_day = None


###############################################################################
# MotDApp #####################################################################
class MotDApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.master = master
        clock.init_values()

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

        self.font = Font(family=CONFIG.FONTS.FAMILY, size=CONFIG.FONTS.SIZE_NORMAL)

        if message_of_the_day is not None:
            self.text = tk.Label(self.frame, text=message_of_the_day,
                                 font=self.font,
                                 foreground=CONFIG.COLORS.FONT,
                                 background=CONFIG.COLORS.BACKGROUND)
            self.text.pack()

        # self.drawPicture(self.frame, "ei01.jpg", 0.55)
        # self.drawPicture(self.frame, "calimero.png", 0.55)
        self.drawPicture(self.frame, "timon_kapitaen.jpg", 0.12)
        self.datetime(self.frame)

        clock.start()

    def drawPicture (self, frame, picture, zoom):
        picture = PIL.Image.open(picture)
        w, h = map(lambda x: int(x*zoom), picture.size)
        picture = picture.resize((w, h), PIL.Image.ANTIALIAS)
        self.image = PIL.ImageTk.PhotoImage(picture)

        self.pic = tk.Label(frame, image=self.image)
        self.pic.pack()

    def datetime (self, frame):
        self.date_text = tk.Label(frame, textvariable=clock.date_date, font=self.font,
                                  foreground=CONFIG.COLORS.FONT, background=CONFIG.COLORS.BACKGROUND)
        self.time_text = tk.Label(frame, textvariable=clock.date_time, font=self.font,
                                  foreground=CONFIG.COLORS.FONT, background=CONFIG.COLORS.BACKGROUND)
        self.date_text.pack()
        self.time_text.pack()


###############################################################################
# Message of the Day ##########################################################
class MotD (object):
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
        self.app = MotDApp(master=self.root)

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
    clock.stop()
    clock.join()
    motd.stop()
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

    clock  = Clock()

    motd = MotD()
    motd.run()

# eof #

