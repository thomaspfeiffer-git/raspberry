#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Circulation.py                                                              #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2020, 2024, 2025       #
###############################################################################

"""
Controls the circulation pump by an html interface.
"""

### Usage ###
# nohup ./Circulation.py [--production] 2>&1 > circulation.log &


### Packages you might need to install ###
# sudo apt install python3-flask
# sudo apt install python3-gpiozero


import argparse
from datetime import datetime, timedelta
from flask import Flask, render_template, request
from gpiozero import Button, LED
import sys
import threading
import time


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown


app = Flask(__name__)


###############################################################################
# CONFIG ######################################################################
class CONFIG:
    class LED:
        on = "BOARD11"
        off = "BOARD13"
    class Relais:
        pump = "BOARD15"
    class Button:
        pump = "BOARD16"


###############################################################################
# Timer #######################################################################
class Timer (object):
    def __init__ (self):
        self.off()

    def on (self, time_=30):
        self.on_until = datetime.now() + timedelta(seconds=time_*60)

    def off (self):
        self.on_until = datetime(1970, 1, 1)

    @property
    def status (self):
        if datetime.now() < self.on_until:
            return self.on_until
        else:
            return 0

###############################################################################
###############################################################################
class Control_Input (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self.button = Button(CONFIG.Button.pump)
        self.button.when_pressed = self.toggle_func()
        self._running = False

    def toggle_func (self):
        def toggle ():
            if timer.status != 0:
                timer.off()
                Log("Manually switched off by button")
            else:
                timer.on()
                Log("Manually switched on by button")
        return toggle

    def run (self):
        self._running = True
        while self._running:
            time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# Control_Output ##############################################################
class Control_Output (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self.led_on  = LED(CONFIG.LED.on)
        self.led_off = LED(CONFIG.LED.off)
        self.relais  = LED(CONFIG.Relais.pump)
        self._running = False

    def run (self):
        self._running = True

        last = None
        while self._running:
            actual = timer.status
            if actual != last:
                if actual != 0:
                    self.led_on.on()
                    self.relais.on()
                    self.led_off.off()
                    Log(f"Circulation pump on until {actual.strftime('%H:%M:%S')}.")
                else:
                    self.led_on.off()
                    self.relais.off()
                    self.led_off.on()
                    Log("Circulation pump off.")
                last = actual

            time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# Flask stuff #################################################################
@app.route('/', methods=['POST', 'GET'])
def HTTP_Control ():
    if request.method == 'POST':
        action = request.form['action']
        Log(f"request: {action}")
        if action == "off":
            timer.off()
        elif action == "status":
            pass
        else:
            action, duration = action.split(":")
            if action == "on":
                timer.on(int(duration))

    if timer.status != 0:
        on_until = timer.status.strftime("%H:%M:%S")
    else:
        on_until = "ausgeschaltet"
    return render_template('control_circulation.html', on_until=on_until)

@app.route('/on')
def API_On ():
    Log("On requested.")
    timer.on(55)
    return "OK.\n"

@app.route('/off')
def API_Off ():
    Log("Off requested.")
    timer.off()
    return "OK.\n"


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    control_input.stop()
    control_input.join()
    control_output.stop()
    control_output.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    parser = argparse.ArgumentParser()
    parser.add_argument("--production", help="run in production (port 80)", action="store_true")
    args = parser.parse_args()

    timer = Timer()
    control_output = Control_Output()
    control_output.start()

    control_input = Control_Input()
    control_input.start()

    if args.production:
        app.run(host="0.0.0.0", port=80)
    else:
        app.run(host="0.0.0.0")

# eof #

