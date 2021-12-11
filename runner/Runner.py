#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Runner.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2021                              #
###############################################################################
"""
willhaben christmas runner:
count rounds during willhaben christmas party.
"""


### usage ###
# nohup ./Runner.py 2>&1 >runner.log &


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
    distance = 194   # Peter Hanisch, 9th Dec 2021
    auto_start = True

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
        self.elapsed_time = "n/a"
        self.round_time = "n/a"
        self.pace = "n/a"
        self.pace_round = "n/a"
        self.distance = 0
        self.started = False

    def init_tk_values (self, master):
        self.tk_start_time = tkinter.StringVar(master)
        self.tk_elapsed_time = tkinter.StringVar(master)
        self.tk_round_time = tkinter.StringVar(master)
        self.tk_timings = tkinter.StringVar(master)
        self.tk_rounds = tkinter.StringVar(master)
        self.tk_paces = tkinter.StringVar(master)
        self.tk_distance = tkinter.StringVar(master)

        self.rounds = 0

    def start (self):
        self.starttime = self.starttime_round = datetime.now()
        self.tk_start_time.set(self.starttime.strftime('%H:%M:%S'))
        self.started = True
        Log("Started.")

    def timings (self):
        if self.started:
            self.elapsed_time = str(datetime.now()-self.starttime).split('.', 2)[0]
        self.tk_elapsed_time.set(self.elapsed_time)
        self.tk_timings.set(f"{self.elapsed_time} | {self.round_time}")
        self.tk_paces.set(f"{self.pace} | {self.pace_round}")

    @staticmethod
    def calc_pace (distance, minutes, seconds):
        distance /= 1000
        minutes += seconds/60
        pace_minutes = int(minutes // distance)
        pace_seconds = round(((minutes / distance) - pace_minutes) * 60)
        return f"{pace_minutes}:{pace_seconds:02}"

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

            t = list(map(int, self.elapsed_time.split(':')))
            self.pace = self.calc_pace(distance=self.distance,
                                       minutes=t[0]*60+t[1], seconds=t[2])

            now = datetime.now()
            d = (str(now-self.starttime_round).split('.', 2)[0]).split(':')
            self.round_time = f"{d[1]}:{d[2]}"
            self.tk_round_time.set(self.round_time)
            self.starttime_round = now

            t = list(map(int, self.round_time.split(':')))
            self.pace_round = self.calc_pace(distance=CONFIG.distance,
                                             minutes=t[0], seconds=t[1])

            Log(f"Round #{self.rounds}")


###############################################################################
# Sender ######################################################################
class Sender (object):
    """Sends data (html, csv) via ssh/scp to http servers.
       Data is shown in the live stream during the event."""
    def __init__ (self):
        self.filename_csv = "counter.txt"
        self.filename_html = "counter.html"

        self.user = "thomas"
        self.host1 = "arverner.smtp.at"
        self.directory1 = "www/sonstiges/"
        self.host2 = "ssh.rekmp.net"
        self.directory2 = "public_html/"

    def scp (self, destination):
        subprocess.run(["scp", f"{self.filename_html}",
                        f"{self.filename_csv}", destination])

    def send (self, data):
        Log(f"Sending data: {data.csv}".replace('\n',' '))
        subprocess.run(["bash", "-c", f"echo \"{data.csv}\" > {self.filename_csv}"])
        subprocess.run(["bash", "-c", f"echo \"{data.html}\" > {self.filename_html}"])
        t1 = threading.Thread(target=self.scp,
                              args=(f"{self.user}@{self.host1}:{self.directory1}",))
        t2 = threading.Thread(target=self.scp,
                              args=(f"{self.user}@{self.host2}:{self.directory2}",))
        t1.start()
        t2.start()
        t1.join
        t2.join


###############################################################################
# Data ########################################################################
class Data (object):
    """Data (html, csv) sent to http servers."""
    def __init__ (self):
        now = datetime.now().strftime('%H:%M:%S')
        self.__csv = "Rounds,Distance (m),Distance (km),Elapsed Time,Round Time,Pace,Pace Last Round,Timestamp\n" + \
                     f"{statistics.rounds}," + \
                     f"{statistics.distance}," + \
                     f"{statistics.distance/1000:.2f}," + \
                     f"{statistics.elapsed_time}," + \
                     f"{statistics.round_time}," + \
                     f"{statistics.pace}," + \
                     f"{statistics.pace_round}," + \
                     f"{now}\n"

        self.__html = "<html>\n" + \
                      "<head>\n" + \
                      "<meta http-equiv='refresh' content='5' />\n" + \
                      "<title>willhaben Christmas</title>\n" + \
                      "<style>\n table, th, td { border: 1px solid black; border-collapse: collapse; }\n</style>\n" + \
                      "</head>\n" + \
                      "<body>\n" + \
                      "<table style='width:75%'>\n" + \
                      "<tr><th>Rounds</th><th>Distance (m)</th><th>Distance (km)</th><th>Elapsed Time</th><th>Round Time</th><th>Pace</th><th>Pace Last Round</th><th>Timestamp</th></tr>\n" + \
                      f"<tr><td>{statistics.rounds}</td>\n" + \
                      f"    <td>{statistics.distance}</td>\n" + \
                      f"    <td>{statistics.distance/1000:.2f}</td>\n".replace('.',',') + \
                      f"    <td>{statistics.elapsed_time}</td>\n" + \
                      f"    <td>{statistics.round_time}</td>\n" + \
                      f"    <td>{statistics.pace}</td>\n" + \
                      f"    <td>{statistics.pace_round}</td>\n" + \
                      f"    <td>{now}</td></tr>\n" + \
                      "</table>\n" + \
                      "</body>\n" + \
                      "</html>\n"

    @property
    def csv (self):
        return self.__csv

    @property
    def html (self):
        return self.__html


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

    def sound (self):
        subprocess.run(["mpg321", "-g 100", "-q", "applause3.mp3"])

    def pressed (self):
        if not statistics.started:
            Log("Not started.")
        elif (datetime.now()-self.last_pressed).seconds > 2:  # Debouncing
            self.last_pressed = datetime.now()
            statistics.rounds += 1

            # Have applause and updating data/csv in parallel #
            t = threading.Thread(name=f"thread-mpg321", target=self.sound)
            t.start()
            self.sender.send(Data())
            t.join()
        else:
            Log("Do not press button too fast!")

    def run (self):
        # Send initial data (0 rounds, 0 km) on start of program. #
        self.sender.send(Data())
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

        self.paces = tkinter.Label(self.screen, textvariable=statistics.tk_paces,
                                   foreground=CONFIG.COLORS.fg,
                                   background=CONFIG.COLORS.bg,
                                   font=self.font_timing)
        self.paces.pack()
        self.add_spacer()
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
        if CONFIG.auto_start:
            statistics.start()
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

