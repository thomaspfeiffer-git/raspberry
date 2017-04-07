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

        self.frame = tk.Frame(self)
        self.frame.grid(sticky="we")
        self.text = tk.Label(self.frame, text="Frohe Ostern!", anchor="center",
                             foreground="black", background="yellow")
        self.text.grid(sticky="we")

        self.drawPicture(self.frame, "ei01.jpg", 0.5)


    def drawPicture (self, frame, picture, zoom):
        picture = PIL.Image.open(picture)
        w, h = map(lambda x: int(x*zoom), picture.size)
        picture = picture.resize((w, h), PIL.Image.ANTIALIAS)

        self.image = PIL.ImageTk.PhotoImage(picture)
        self.pic = tk.Label(frame, image=self.image, justify="center", anchor="center", background="yellow")
        self.pic.grid(sticky="we") 


###############################################################################
# Timer #######################################################################
class Timer (object):
    def __init__ (self):
        self.root = tk.Tk()

        self.root.overrideredirect(1)
        self.root.config(cursor='none')
        self.root.resizable(width=False, height=False)

        self.root.width  = 350
        self.root.height = 250
        self.root.borderwidth = 10

        self.root.geometry("300x250+10+10")
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

