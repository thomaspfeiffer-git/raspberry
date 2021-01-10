#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# ping.py                                                                     #
# (c) https://github.com/thomaspfeiffer-git 2021                              #
###############################################################################
"""
Pings a various number of hosts.
Is used standalone, thus no libraries are included (eg Log and Shutdown).
"""

from datetime import datetime
import shlex
import signal
import subprocess
import sys
import threading
import time


hosts = ["arverner.smtp.at", "orf.at"]
ping_threads = []

ping_command = "ping -c 1 {}"


###############################################################################
# Log #########################################################################
def Log(logstr):
    """improved log output"""
    print("{}: {}".format(datetime.now().strftime("%Y%m%d %H:%M:%S"), logstr))


###############################################################################
# Shutdown ####################################################################
class Shutdown(object):
    def __init__(self, shutdown_func):
        self.shutdown_func = shutdown_func
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def shutdown(self, __s, __f):
        self.shutdown_func()


###############################################################################
# Ping ########################################################################
class Ping(threading.Thread):
    def __init__(self, host, log_lock):
        threading.Thread.__init__(self)
        self.host = host
        self.lock = log_lock
        self.command = shlex.split(ping_command.format(self.host))

    def run(self):
        self._running = True

        while self._running:
            with subprocess.Popen(self.command, stdout=subprocess.PIPE) as process:
                result = process.stdout.read().decode(encoding='UTF-8').split('\n')
            with self.lock:
                Log(f"{result[1]}")
            time.sleep(1)

    def stop(self):
        self._running = False


###############################################################################
# shutdown_application ########################################################
def shutdown_application():
    """called on shutdown; stops all threads"""
    Log("Stopping application.")
    for thread in ping_threads:
        thread.stop()
        thread.join()
    Log("Application stopped.")
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    log_lock = threading.Lock()
    shutdown = Shutdown(shutdown_func=shutdown_application)

    for host in hosts:
        ping_threads.append(Ping(host, log_lock))
        ping_threads[-1].start()

    while True:      # keep main thread alive
        time.sleep(0.1)

# eof #
