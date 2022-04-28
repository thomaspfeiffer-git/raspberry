#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Radio.py                                                                    #
# (c) https://github.com/thomaspfeiffer-git 2021, 2022                        #
###############################################################################
"""
"""

### usage ###
# ./Radio.py 2>&1 > radio.log &


import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font

from collections import OrderedDict
from flask import Flask
from functools import wraps
import os
import subprocess
import sys
import threading
import time
from werkzeug.serving import make_server

sys.path.append('../../libs')
from Shutdown import Shutdown
from Logging import Log

sys.path.append('../libraries')
from touchevent import Touchevent
from sound import Sound

from config import CONFIG

app = Flask(__name__)


station_name = "name"
station_url  = "url"
Stations = OrderedDict()
Stations.update({ 's1': { station_name: "88.6", station_url: "https://edge07.streamonkey.net/radio886-onair/stream/mp3" } })
Stations.update({ 's2': { station_name: "Ö3", station_url: "https://orf-live.ors-shoutcast.at/oe3-q2a" } })
Stations.update({ 's3': { station_name: "Radio Wien", station_url: "https://orf-live.ors-shoutcast.at/wie-q2a" } })
Stations.update({ 's4': { station_name: "Lounge FM", station_url: "https://s35.derstream.net/ukwwien.mp3" } })
Stations.update({ 's5': { station_name: "The Sound of New York City", station_url: "http://ic2377.c900.fast-serv.com/tsonyc.mp3" } })
Stations.update({ 's6': { station_name: "BBC Radio 2", station_url: "https://stream.live.vc.bbcmedia.co.uk/bbc_radio_two" } })
Stations.update({ 's7': { station_name: "Downbeat Radio", station_url: "https://stream.laut.fm/lounge" } })
Stations.update({ 's8': { station_name: "DeepLazz Radio", station_url: "http://stream.zenolive.com/m32839kywrquv" } })

# ORF1: https://orf1.mdn.ors.at/out/u/orf1/q6a/manifest.m3u8
# ORF2: https://orf2.mdn.ors.at/out/u/orf2/q6a/manifest.m3u8
#       https://orf2.mdn.ors.at/out/u/orf2/q4a/manifest.m3u8
# ORF3: https://orf3.mdn.ors.at/out/u/orf3/q6a/manifest.m3u8
# http://blog.peterseil.com/orf-stream-links/

###############################################################################
###############################################################################
def set_volume (volume:int = 25):
    """sets the volume [percent]
       shell command: amixer -D pulse sset Master 50%
    """
    if not 0 <= volume <= 100:
        raise ValueError(f"volume is {volume}, must be in 0..100")

    command = ["amixer", "-D", "pulse", "sset", "Master", f"{volume}%"]
    process = subprocess.Popen(command)
    process.wait()
    process.communicate()


###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    def __init__ (self, master):
        threading.Thread.__init__(self)
        self.master = master
        self.__volume = CONFIG.APPLICATION.VOLUME_DEFAULT
        set_volume(self.__volume)
        self.radio_process = None
        self.timestamp = time.time()
        self.window_hidden = False

    def triggered (func):
        @wraps(func)
        def trigger (self, *args, **kwargs):
            self.timestamp = time.time()
            func(self, *args, **kwargs)
        return trigger

    @triggered
    def show_window (self):
        self.master.deiconify()
        self.window_hidden = False

    def hide_window (self):
        if not self.window_hidden:
            self.master.withdraw()
            self.window_hidden = True

    @property
    def volume (self):
        return self.__volume

    @triggered
    def adjust_volume (self, value):
        self.__volume += value
        if self.__volume > 100: self.__volume = 100
        if self.__volume < 0: self.__volume = 0
        set_volume(self.__volume)

    @triggered
    def play (self, station_url):
        if Touchevent.event():   # brightness control
            Sound.play(CONFIG.CLICK_SOUND)

            Log(f"Playing {station_url}")
            if self.radio_process is not None:
                self.stop_play()

            self.radio_process = subprocess.Popen(["cvlc", station_url])

    @triggered
    def stop_play (self, nosound=False):
        if Touchevent.event():   # brightness control
            if not nosound:
                Sound.play(CONFIG.CLICK_SOUND)

            Log("Stopping radio station.")
            if self.radio_process:
                self.radio_process.terminate()
                self.radio_process.communicate()
                self.radio_process = None

    def run (self):
        self._running = True

        while self._running:
            time.sleep(0.1)
            if self.timestamp + CONFIG.APPLICATION.DELAY_TO_HIDE < time.time():
                self.hide_window()

        self.stop_play(nosound=True)

    def stop (self):
        self._running = False


###############################################################################
# Radio_TK ####################################################################
class Radio_TK (tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)

        self.master = master
        self.frame  = tk.Frame(self.master, bg=CONFIG.COLORS.BACKGROUND,
                               width=CONFIG.COORDINATES.WIDTH,
                               height=CONFIG.COORDINATES.HEIGHT,
                               borderwidth=25,
                               highlightthickness=5,
                               highlightbackground=CONFIG.COLORS.BORDER)
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

    def create_tk_elements (self):
        self.style = ttk.Style()
        self.style.configure("Radio.TButton",
                             font=(CONFIG.FONTS.FAMILY, CONFIG.FONTS.SIZE_NORMAL),
                             width=15, background=CONFIG.COLORS.BUTTON)
        self.style.map("Radio.TButton", background=[('active', CONFIG.COLORS.BUTTON)],
                                        relief=[('pressed', 'groove'),
                                                ('!pressed', 'ridge')])
        self.style.configure("Off.Radio.TButton",
                             font=(CONFIG.FONTS.FAMILY, CONFIG.FONTS.SIZE_NORMAL),
                             width=10, background=CONFIG.COLORS.BUTTON_OFF)
        self.style.map("Off.Radio.TButton", background=[('active', CONFIG.COLORS.BUTTON_OFF)],
                                            relief=[('pressed', 'groove'),
                                                    ('!pressed', 'ridge')])
        self.style.configure("Volume.Radio.TButton",
                             font=(CONFIG.FONTS.FAMILY, CONFIG.FONTS.SIZE_NORMAL),
                             width=8, background=CONFIG.COLORS.BUTTON_VOLUME)
        self.style.map("Volume.Radio.TButton", background=[('active', CONFIG.COLORS.BUTTON_VOLUME)],
                                            relief=[('pressed', 'groove'),
                                                    ('!pressed', 'ridge')])
        frame_stations = tk.Frame(master=self.frame)
        frame_stations.pack()

        i = 0
        self.buttons = OrderedDict()
        for station in Stations:
            frame = tk.Frame(master=frame_stations)
            frame.grid(row=i // 2, column=i % 2)

            self.buttons.update({station: ttk.Button(frame, text=Stations[station][station_name],
                                                     style="Radio.TButton",
                                                     command=lambda url=Stations[station][station_url]: radio.control.play(url))})
            i += 1

        frame_control_master = tk.Frame(master=self.frame)
        frame_control_master.pack()
        frame_control = []
        for i in range(3):
            frame_control.append(tk.Frame(master=frame_control_master))
            frame_control[i].grid(row=0, column=i)

        self.buttons.update({'off': ttk.Button(frame_control[1], text="Ausschalten",
                                               style="Off.Radio.TButton", command=lambda: radio.control.stop_play())})
        self.buttons.update({'vol_minus': ttk.Button(frame_control[0], text="Leiser",
                                               style="Volume.Radio.TButton", command=lambda: radio.control.adjust_volume(-5))})
        self.buttons.update({'vol_plus': ttk.Button(frame_control[2], text="Lauter",
                                               style="Volume.Radio.TButton", command=lambda: radio.control.adjust_volume(+5))})

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
        self.app = Radio_TK(master=self.root)

        self.control = Control(self.root)
        self.control.start()

    def poll (self):
        """polling needed for ctrl-c"""
        self.root.pollid = self.root.after(50, self.poll)

    def run (self):
        """start polling and run application"""
        self.root.pollid = self.root.after(50, self.poll)
        self.app.mainloop()

    def stop (self):
        self.control.stop()
        self.control.join()

        self.root.after_cancel(self.root.pollid)
        self.root.destroy()
        self.root.quit()


###############################################################################
# FlaskThread #################################################################
class FlaskThread (threading.Thread):
    def __init__ (self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('0.0.0.0', CONFIG.APPLICATION.PORT, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run (self):
        Log("Starting flask server.")
        self.srv.serve_forever()

    def shutdown (self):
        self.srv.shutdown()


###############################################################################
# Flask stuff #################################################################
@app.route('/showapp')
def API_ShowApp ():
    radio.control.show_window()
    return "OK.\n"

@app.route('/hideapp')
def API_HideApp ():
    radio.control.hide_window()
    return "OK.\n"

@app.route('/radiooff')
def API_RadioOff ():
    radio.control.stop_play(nosound=True)
    return "OK.\n"


###############################################################################
# shutdown_application ########################################################
def shutdown_application ():
    """called on shutdown; stops all threads"""
    Log("Stopping application.")
    flask_server.shutdown()
    radio.stop()
    Log("Application stopped.")
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

    flask_server = FlaskThread(app)
    flask_server.start()

    radio = Radio()
    radio.run()

# eof #

