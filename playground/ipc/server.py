#!/usr/bin/python


from SensorQueue import SensorQueueServer


###############################################################################
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    SensorServer.stop()
    SensorServer.join()
    print("Exit")
    sys.exit()



def _Exit(__s, __f):
    """exit for signal handler"""
    print("_Exit")
    Exit()



###############################################################################
signal.signal(signal.SIGTERM, _Exit)



SensorServer = SensorQueueServer()
ServerServer.start()

