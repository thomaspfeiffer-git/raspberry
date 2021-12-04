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
    distance = 247

    def __init__ (self, rounds):
        self.__csv = f"{rounds};{rounds*self.distance};" + \
                     f"{rounds*self.distance/1000:.2f} km;".replace('.',',') + \
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
        self.rounds = 0
        self.sender = Sender()
        self.button = Button(4)
        self.button.when_pressed = lambda: self.pressed()
        signal.signal(signal.SIGUSR1, lambda s, f: self.pressed())
        self._running = False

    def init_values (self, master):
        self.rounds_tk = tkinter.StringVar(master)
        self.rounds_tk.set(self.rounds)

    def display (self):
        display.print(f"Rounds: {self.rounds}",
                      f"IP: {MyIP()}",
                      f"Time: {datetime.now().strftime('%H:%M:%S')}")

    def pressed (self):
        self.rounds += 1
        Log(f"Round #{self.rounds}")
        self.rounds_tk.set(self.rounds)
        self.sender.send(Data(self.rounds))
        # subprocess.run(["mpg321", "-g 100", "-q", "applause3.mp3"])

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

        self.font = Font(family="Arial", size=400, weight="bold")

        self.screen = tkinter.Frame(self.master)
        self.screen.config(bg="white", width=self.master.width,
                                       height=self.master.height)

        counter.init_values(self)
        counter.start()
        self.rounds = counter.rounds_tk

        self.text = tkinter.Label(self.screen, textvariable=self.rounds,
                                  foreground="red", background="white",
                                  font=self.font)
        self.text.place(relx=.5, rely=.5, anchor="center")

        self.screen.grid()


###############################################################################
# Screen ######################################################################
class Screen (object):
    """  """
    def __init__ (self):
        self.root = tkinter.Tk()
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

    counter = Counter()
    display = Display1306()
    screen = Screen()
    screen.run()

# eof #

