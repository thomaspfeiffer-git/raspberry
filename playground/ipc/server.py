#!/usr/bin/python

import signal
from SensorQueue import SensorQueueServer


###############################################################################
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    print("Exit")
    SensorServer.stop()
    SensorServer.join()
    sys.exit()



def _Exit(__s, __f):
    """exit for signal handler"""
    print("_Exit")
    Exit()



###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)
    SensorServer = SensorQueueServer()

    try:
        SensorServer.start()
        print "server started"
        while (True):
            pass

    except KeyboardInterrupt:
        Exit()

    except SystemExit:                  # Done in signal handler (method _Exit()) #
        pass

    except:
        print(traceback.print_exc())

    finally:        # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

### eof ###

