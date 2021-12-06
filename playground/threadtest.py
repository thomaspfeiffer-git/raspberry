#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# threadtest.py                                                               #
# (c) https://github.com/thomaspfeiffer-git 2021                              #
###############################################################################
""" """

import sys
import threading
import time

sys.path.append('../libs')
from Logging import Log


def thread(id_):
    Log(f"Anfang von Thread {id_}")
    time.sleep(id_)
    Log(f"Ende von Thread {id_}")


if __name__ == '__main__':
    for i in range(5):
        threading.Thread(name=f"Thread #{i}", target=thread, args=(i,)).start()

    main_thread = threading.main_thread()

    while True:
        for t in threading.enumerate():
            time.sleep(0.25)
            if t is main_thread:
                continue
            Log(f"Joining {t.getName()}")
            t.join(0.1)
            Log(f"Thread '{t.getName()}' is alive: {t.isAlive()}")

# eof #
