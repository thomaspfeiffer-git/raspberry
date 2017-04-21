#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# MessageOfTheDay.py                                                          #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
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


###############################################################################
# TimerApp ####################################################################
class TimerApp (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.master = master
        self.grid()


        self.font  = Font(family="Arial", size=20)
        self.frame = tk.Frame(self)    # TODO: configfile
        self.frame.config(width=410, height=480, background="LightSkyBlue")
        self.frame.grid_propagate(0)
        self.frame.grid()
#        self.text = tk.Label(self.frame, text="Frohe Ostern!", font=self.font,
#                             anchor="center", justify="center",
#                             foreground="black", background="yellow")
#        self.text.grid(sticky="we")

        # self.drawPicture(self.frame, "ei01.jpg", 0.55)
        # self.drawPicture(self.frame, "calimero.png", 0.55)
        self.drawPicture(self.frame, "timon_kapitaen.jpg", 0.15)


    def drawPicture (self, frame, picture, zoom):
        picture = PIL.Image.open(picture)
        w, h = map(lambda x: int(x*zoom), picture.size)
        picture = picture.resize((w, h), PIL.Image.ANTIALIAS)

        self.image = PIL.ImageTk.PhotoImage(picture)  # TODO: width=<configfile>
        self.pic = tk.Label(frame, image=self.image, width=410, justify="center", anchor="center", background="LightSkyBlue")
        self.pic.grid(sticky="we") 


###############################################################################
# Timer #######################################################################
class Timer (object):  # TODO: rename
    def __init__ (self):
        self.root = tk.Tk()

        self.root.overrideredirect(1)
        self.root.config(cursor='none')
        self.root.resizable(width=False, height=False)

        # self.root.width  = 520   # TODO: config file
        self.root.width  = 410   # TODO: config file
        self.root.height = 480
        self.root.borderwidth = 10

        # self.root.geometry("520x500+280+0")   # TODO: config file
        self.root.geometry("410x480+280+0")   # TODO: config file
        self.root.config(bg="LightSkyBlue")
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

