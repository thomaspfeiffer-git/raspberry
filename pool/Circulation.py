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


from flask import Flask, render_template
import sys


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown


app = Flask(__name__)


###############################################################################
# Flask stuff #################################################################
@app.route('/')
def Control ():
    from datetime import datetime
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

    # app.run(host="0.0.0.0", port=80)
    app.run(host="0.0.0.0")

# eof #

