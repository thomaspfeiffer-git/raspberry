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
# sudo pip3 install Pillow
#
# turn off screen saver:
# sudo apt-get install xscreensaver
# start xscreensaver and set screensaver off manually


from datetime import datetime
from gpiozero import Button
import os
import signal
import subprocess
import sys
import threading
import time
import tkinter
from tkinter.font import Font

sys.path.append('../libs')
from Commons import Display1306, MyIP
from Shutdown import Shutdown
from Logging import Log


###############################################################################
# CONFIG ######################################################################
class CONFIG:
    distance = 247

    class COLORS:
        bg = "white"
        fg = "red"
        bg_btn_start = "light green"


###############################################################################
# Statistics ##################################################################
class Statistics (object):
    def __init__ (self):
        self.starttime = None
        self.starttime_round = None
        self.__rounds = 0
        self.round_time = "n/a"
        self.distance = 0
        self.started = False

    def init_tk_values (self, master):
        self.tk_start_time = tkinter.StringVar(master)
        self.tk_elapsed_time = tkinter.StringVar(master)
        self.tk_round_time = tkinter.StringVar(master)
        self.tk_timings = tkinter.StringVar(master)
        self.tk_rounds = tkinter.StringVar(master)
        self.tk_distance = tkinter.StringVar(master)

        self.rounds = 0

    def start (self):
        self.starttime = self.starttime_round = datetime.now()
        self.tk_start_time.set(self.starttime.strftime('%H:%M:%S'))
        self.started = True
        Log("Started.")

    def timings (self):
        if self.started:
            elapsed_time = str(datetime.now()-self.starttime).split('.', 2)[0]
        else:
            elapsed_time = "0:00:00"
        self.tk_elapsed_time.set(elapsed_time)
        self.tk_timings.set(f"{elapsed_time} | {self.round_time}")

    @property
    def rounds (self):
        return self.__rounds

    @rounds.setter
    def rounds (self, value):
        if not self.started:
            self.tk_rounds.set(0)
            Log("Not started.")
        else:
            self.__rounds = value
            self.tk_rounds.set(self.rounds)
            self.distance = self.rounds * CONFIG.distance
            self.tk_distance.set(self.distance)

            now = datetime.now()
            d = (str(now-self.starttime_round).split('.', 2)[0]).split(':')
            self.round_time = f"{d[1]}:{d[2]}"
            self.starttime_round = now

            self.tk_round_time.set(self.round_time)

            Log(f"Round #{self.rounds}")


###############################################################################
# Sender ######################################################################
class Sender (object):
    """ """
    def __init__ (self):
        self.filename  = "counter.txt"
        self.user      = "thomas"
        self.host      = "arverner.smtp.at"
        self.directory = "www/sonstiges/"

    def send (self, data):
        Log(f"Sending to host {self.host}: {data.csv}")
        subprocess.run(["bash", "-c", f"echo \"{data.csv}\" > {self.filename}"])
        subprocess.run(["scp", f"{self.filename}",
                               f"{self.user}@{self.host}:{self.directory}"])


###############################################################################
# Data ########################################################################
class Data (object):
    """ """
    def __init__ (self):   # TODO: use statistics.distance
        self.__csv = f"{statistics.rounds};{statistics.rounds*CONFIG.distance};" + \
                     f"{statistics.rounds*CONFIG.distance/1000:.2f} km;".replace('.',',') + \
                     f"{datetime.now().strftime('%H:%M:%S')}"

    @property
    def csv (self):
        return self.__csv


###############################################################################
# Counter #####################################################################
class Counter (threading.Thread):
    """ """
    def __init__ (self):
        threading.Thread.__init__(self)
        self.sender = Sender()
        self.last_pressed = datetime.now()
        self.button = Button(4)
        self.button.when_pressed = lambda: self.pressed()
        signal.signal(signal.SIGUSR1, lambda s, f: self.pressed())
        self._running = False

    def display (self):
        display.print(f"Rounds: {statistics.rounds}",
                      f"IP: {MyIP()}",
                      f"Time: {datetime.now().strftime('%H:%M:%S')}")

    def pressed (self):
        if (datetime.now()-self.last_pressed).seconds > 2:  # Debouncing
            self.last_pressed = datetime.now()
            statistics.rounds += 1
            self.sender.send(Data())
            # subprocess.run(["mpg321", "-g 100", "-q", "applause3.mp3"])
        else:
            Log("Do not press button too fast!")

    def run (self):
        self._running = True
        while self._running:
            self.display()
            time.sleep(0.1)

        self.button.close()
        display.off()

    def stop (self):
        self._running = False


###############################################################################
# ScreenApp ###################################################################
class ScreenApp (tkinter.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.master = master
        self.spacer = []

        self.font = Font(family="Arial", size=300, weight="bold")
        self.font_timing = Font(family="Arial", size=80)
        self.font_button = Font(family="Arial", size=18)

        self.screen = tkinter.Frame(self.master)
        self.screen.config(bg=CONFIG.COLORS.bg, width=self.master.width,
                           height=self.master.height)

        statistics.init_tk_values(self)
        counter.start()

        self.rounds = tkinter.Label(self.screen, textvariable=statistics.tk_rounds,
                                    foreground=CONFIG.COLORS.fg,
                                    background=CONFIG.COLORS.bg,
                                    font=self.font)
        self.rounds.pack()

        self.timings = tkinter.Label(self.screen, textvariable=statistics.tk_timings,
                                     foreground=CONFIG.COLORS.fg,
                                     background=CONFIG.COLORS.bg,
                                     font=self.font_timing)
        self.timings.pack()

        for _ in range(4):
            self.add_spacer()

        self.button_start = tkinter.Button(self.screen, text="Start",
                                           bg=CONFIG.COLORS.bg_btn_start,
                                           font=self.font_button,
                                           width=50, height=2,
                                           command=lambda: statistics.start())
        self.button_start.pack()
        self.add_spacer()

        self.button_reset = tkinter.Button(self.screen, text="Reset Counter",
                                           fg=CONFIG.COLORS.fg, font=self.font_button,
                                           width=50, height=2,
                                           command=lambda: self.set_counter(0))
        self.button_reset.pack()
        self.add_spacer()

        value = tkinter.StringVar(self.screen)
        self.entry = tkinter.Entry(self.screen, textvariable=value,
                                   width=50, font=self.font_button)
        self.entry.pack(pady=10)

        self.button_set = tkinter.Button(self.screen, text="Set Counter",
                                         fg=CONFIG.COLORS.fg, font=self.font_button,
                                         width=50, height=2,
                                         command=lambda: self.set_counter(value.get()))
        self.button_set.pack()

        self.screen.pack(expand=True)

    def add_spacer (self):
        self.spacer.append(tkinter.Label(self.screen, text="", bg=CONFIG.COLORS.bg).pack())

    def set_counter (self, value):
        try:
            counter.rounds = int(value)
        except ValueError:
            Log(f"Value '{value}' is not an integer.")
        else:
            Log(f"Manually set counter to {value}.")


###############################################################################
# Screen ######################################################################
class Screen (object):
    """  """
    def __init__ (self):
        self.root = tkinter.Tk()
        self.root.overrideredirect(1)
        self.root.resizable(width=False, height=False)

        self.root.width  = self.root.winfo_screenwidth()
        self.root.height = self.root.winfo_screenheight()
        self.root.borderwidth = 10
        self.root.geometry("{}x{}+{}+{}".format(self.root.width,
                                                self.root.height, 0, 0))
        self.root.config(bg=CONFIG.COLORS.bg)
        self.app = ScreenApp(master=self.root)

    def poll (self):
        """polling needed for ctrl-c"""
        self.root.pollid = self.root.after(50, self.poll)
        statistics.timings()

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
    Log("Shutdown.")

    display.off()
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

    statistics = Statistics()
    counter = Counter()
    display = Display1306()
    screen = Screen()
    screen.run()

# eof #

