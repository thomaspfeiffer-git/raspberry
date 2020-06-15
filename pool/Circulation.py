#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Circulation.py                                                              #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2020                   #
###############################################################################

"""
"""

### Usage ###
# nohup ./Circulation.py 2>&1 > circulation.log &


from datetime import datetime, timedelta
from flask import Flask, render_template
import sys


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown


app = Flask(__name__)


###############################################################################
# IO ##########################################################################
class IO (object):
    pass


###############################################################################
# Timer #######################################################################
class Timer (object):
    def __init__ (self):
        self.on_until = datetime(1970, 1, 1)

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
# Control #####################################################################
class Control (object):
    def __init__ (self):
        self._running = False

    def run (self):
        # TODO
        self._running = True

        while self._running:
            time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# Flask stuff #################################################################
@app.route('/')
def HTTP_Control ():
    now = datetime.now()
    return render_template('control_circulation.html', now=now)


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")


    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    timer = Timer()

    Log(f"Timerstatus: {timer.status}")
    timer.on()
    Log(f"Timerstatus: {timer.status}")
    timer.off()
    Log(f"Timerstatus: {timer.status}")

    # app.run(host="0.0.0.0", port=80)
#     app.run(host="0.0.0.0")

# eof #

