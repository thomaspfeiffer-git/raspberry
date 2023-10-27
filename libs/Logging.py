# -*- coding: utf-8 -*-
############################################################################
# Logging.py                                                               ä
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017, 2023          #
############################################################################
"""
improved log output
"""

import sys
from datetime import datetime

def Log (logstr, file=sys.stdout):
    print(f"{datetime.now().strftime('%Y%m%d %H:%M:%S')}: {logstr}", file=file)

# eof #

