#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Ventilation.py                                                              #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019, 2020             #
###############################################################################

"""
Controls ventilation of the control room of our swimming pool.
"""

### Usage ###
# nohup ./Ventilation.py 2>&1 > ventilation.log &


### Packages you might need to install ###
# sudo pip3 install Pillow
# sudo pip3 install Flask
# sudo pip3 install xmltodict


from enum import Enum
from flask import Flask, request
import sys
import threading
import time


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown

from Config import CONFIG
from Display import Display
from Fan import Fan
from Schedule import Scheduler, State
from Sensors import Sensors, Sensordata
from Ventilation_UDP import UDP_Sender

app = Flask(__name__)


###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    fan_in1 = "fan_in1"
    fan_in2 = "fan_in2"
    fan_out = "fan_out"
    fan_box = "fan_box"

    class State (Enum):
        off = 0
        on = 1

    def __init__ (self, data, scheduler):
        threading.Thread.__init__(self)
        self.status = Control.State.off
        self.data = data
        self.scheduler = scheduler
        self.run_optional = False
        self.fans = {Control.fan_in1: Fan(CONFIG.Fans.fan_in1, delay=15),
                     Control.fan_in2: Fan(CONFIG.Fans.fan_in2, delay=10),
                     Control.fan_out: Fan(CONFIG.Fans.fan_out, delay=5),
                     Control.fan_box: Fan(CONFIG.Fans.fan_box, delay=0)}
        self._running = True

    def ventilation_on (self):
        self.data.fan1_on = 1
        self.data.fan2_on = 1
        self.data.fan3_on = 1
        self.data.fan4_on = 1
        self.status = Control.State.on
        for f in self.fans.values():
            f.on()

    def ventilation_off (self):
        self.data.fan1_on = 0
        self.data.fan2_on = 0
        self.data.fan3_on = 0
        self.data.fan4_on = 0
        self.status = Control.State.off
        for f in self.fans.values():
            f.off()

    def toggle (self):
        if self.status == Control.State.on:
            self.ventilation_off()
        else:
            self.ventilation_on()

    def run (self):
        last_on = None
        while self._running:
            if self.scheduler.state.state == State.States.on and not last_on:
                self.ventilation_on()
                last_on = True
            elif self.scheduler.state.state == State.States.off and last_on:
                self.ventilation_off()
                last_on = False

            time.sleep(0.5)

    def stop (self):
        for f in self.fans.values():
            f.close(immediate=True)
        self._running = False


###############################################################################
# Flask stuff #################################################################
@app.route('/toggle')
def API_Toggle ():
    triggered_by_button = request.args.get("button", "0") == "1"
    Log(f"Request: toggled; triggered by button: {triggered_by_button}")
    control.toggle()
    return "OK.\n"

@app.route('/schedule')
def API_Schedule ():
    Log("Request: reload schedule")
    scheduler.load_schedule()
    return "OK.\n"


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    control.stop()
    control.join()
    scheduler.stop()
    scheduler.join()
    udp_sender.stop()
    udp_sender.join()
    sensors.stop()
    sensors.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)
    data = Sensordata()

    display = Display(data)

    udp_sender = UDP_Sender(data)
    udp_sender.start()

    sensors = Sensors(data,update_display=display.print)
    sensors.start()

    scheduler = Scheduler(data)
    scheduler.start()

    control = Control(data, scheduler)
    control.start()

    app.run(host="0.0.0.0")

# eof #

