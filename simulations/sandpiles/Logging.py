# -*- coding: utf-8 -*-
############################################################################
# Logging.py                                                               ä
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""
"""

import sys
from datetime import datetime

def Log (logstr, flush=False):
    """improved log output"""
    print("{}: {}".format(datetime.now().strftime("%Y%m%d %H:%M:%S"), logstr))
    if flush:
        sys.stdout.flush()

# eof #

