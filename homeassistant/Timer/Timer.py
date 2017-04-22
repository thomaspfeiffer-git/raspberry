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
import subprocess
import sys
import threading
import time

sys.path.append('../../libs')
from Shutdown import Shutdown
from Logging import Log

from config import CONFIG


###############################################################################
# Sound #######################################################################
class Sound (object):
    """plays a sound
       - mp3: path to mp3 file
       - runs: how often the mp3 file shall be played
    """
    @staticmethod
    def play (mp3, runs=1):
        command = ["mpg321", "-g 100"] + [mp3] * runs
        subprocess.Popen(command) 


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
        self.set_event   = False
        self.reset_event = False
        self.alarm_id    = None

    def create_elements (self, frame):
        self.master = frame
        self.frame  = tk.Frame(self.master, bg=CONFIG.COLORS.BACKGROUND,
                               width=CONFIG.COORDINATES.WIDTH, 
                               height=CONFIG.COORDINATES.HEIGHT)
        self.frame.pack_propagate(0)
        self.frame.pack()
 
        self.style = ttk.Style()
        self.style.configure("Timer.TButton", 
                             font=(CONFIG.FONTS.FAMILY, CONFIG.FONTS.SIZE_NORMAL),
                             width=5, background=CONFIG.COLORS.BUTTON)
        self.style.map("Timer.TButton", background=[('active', CONFIG.COLORS.BUTTON)],
                                        relief=[('pressed', 'groove'),
                                                ('!pressed', 'ridge')])

        self.buttons = OrderedDict()
        self.buttons.update({'p5': ttk.Button(self.frame, text="+5", style="Timer.TButton", command = lambda: self.set_counter(5))})
        self.buttons.update({'p1': ttk.Button(self.frame, text="+1", style="Timer.TButton", command = lambda: self.set_counter(1))})
        self.buttons.update({'m1': ttk.Button(self.frame, text="-1", style="Timer.TButton", command = lambda: self.set_counter(-1))})
        self.buttons.update({'m5': ttk.Button(self.frame, text="-5", style="Timer.TButton", command = lambda: self.set_counter(-5))})
        self.buttons.update({'reset': ttk.Button(self.frame, text="Reset", style="Timer.TButton", command = self.reset_counter)})
        for btn in self.buttons.values():
            btn.pack(padx=5, pady=5)

        self.timer = tk.StringVar()
        self.timerdisplay = ttk.Label(self.frame, textvariable=self.timer, 
                                      style="Timer.TButton")
        self.timerdisplay.pack(padx=5, pady=5)
        self.timerdisplay.pack_forget()

    def set_counter (self, value):
        """sets the counter/countdown
           and displays the countdown to the screen"""
        Sound.play(CONFIG.CLICK_SOUND)
        if self.alarm_id is not None:
            self.set_event = True
        countdown.alter(value*60)
        if countdown.counter > 0:
            self.timerdisplay.pack(padx=5, pady=5)
            self.reset_event = False
    
    def reset_counter (self):
        """resets the timer and switches alarm off"""
        Sound.play(CONFIG.CLICK_SOUND)
        self.reset_event = True
        countdown.reset()
        self.timer.set("")
        self.timerdisplay.pack_forget()

    def alarm_blink (self, counter):
        if counter > 0 and self.__running \
           and not self.reset_event and not self.set_event:
            self.timerdisplay.config(background=
                     CONFIG.ALARM.COLORS[counter % len(CONFIG.ALARM.COLORS)])
            self.alarm_id = self.master.after(CONFIG.ALARM.DELAY, 
                                lambda: self.alarm_blink(counter-1))
        else:
            self.alarm_id = None
            self.timerdisplay.config(background=CONFIG.COLORS.BUTTON)
            if not self.set_event: 
                self.timerdisplay.pack_forget()
            self.set_event = False

    def alarm (self):
        self.timer.set("Alarm")
        self.alarm_id = self.master.after(CONFIG.ALARM.DELAY, 
                                lambda: self.alarm_blink(CONFIG.ALARM.COUNT))
        Sound.play(CONFIG.ALARM.SOUND, runs=3)

    def run (self):
        self.__running = True
        lastvalue = 0
        while self.__running:
            time.sleep(0.1)
            value = countdown.counter
            if value != 0:
                self.timer.set("{:d}:{:02d}".format(value // 60, value % 60))
            if lastvalue != 0 and value == 0 and not self.reset_event:
                self.alarm()
            lastvalue = value
        if self.alarm_id:
           self.master.after_cancel(self.alarm_id)

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

