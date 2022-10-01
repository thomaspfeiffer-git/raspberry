# -*- coding: utf-8 -*-
###############################################################################
# Shutdown.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
###############################################################################
"""provides a simple class for handling SIGTERM and SIGINT."""


"""
Usage:

1) You have a dedicated shutdown function for your application
--------------------------------------------------------------

    shutdown = Shutdown(shutdown_func=shutdown_application)

On SIGTERM or SIGINT, the function shutdown_application() 
will be called.


2) No dedicated shutdown function implemented
---------------------------------------------

    shutdown = Shutdown()
    # ...
    while not shutdown.terminate:
        # do something

    # after shutdown

"""

import signal


class Shutdown (object):
    terminate = False

    def __init__ (self, shutdown_func=None):
        self.shutdown_func = shutdown_func
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def shutdown (self, __s, __f):
        self.terminate = True
        if self.shutdown_func:
             self.shutdown_func()

# eof #

