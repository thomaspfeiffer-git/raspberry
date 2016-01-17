#!/usr/bin/python
###############################################################################
# QueueServer.py                                                              #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Server for messages of sensor values based on SensorQueueServer"""

import signal
import sys
import traceback

sys.path.append('../libs')
from SensorQueue import SensorQueueServer


###############################################################################
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    print("Exit")
    sys.exit()

def _Exit(__s, __f):
    """exit for signal handler"""
    print("_Exit")
    Exit()


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)

    try:
        SensorServer = SensorQueueServer()
        SensorServer.start()

    except KeyboardInterrupt:
        Exit()

    except SystemExit:               # Done in signal handler (method _Exit()) #
        pass

    except:
        print(traceback.print_exc())

    finally:     # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

### eof ###

