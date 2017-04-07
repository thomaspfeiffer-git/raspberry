# -*- coding: utf-8 -*-
############################################################################
# Logging.py                                                               ä
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""
"""

from datetime import datetime

def Log (logstr):
    """improved log output"""
    print("{}: {}".format(datetime.now().strftime("%Y%m%d %H:%M:%S"), logstr))

# eof #

