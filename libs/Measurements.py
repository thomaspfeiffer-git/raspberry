# -*- coding: utf-8 -*-
##############################################################################
# Measurements.py                                                            #
# (c) https://github.com/thomaspfeiffer-git 2015, 2016                       #
##############################################################################
"""provides an extended deque with average() and last()"""

from collections import deque
import sys

class Measurements (deque):
    """extended deque: additional methods for average and last added item"""
    def __init__ (self, maxlen=5):
        super().__init__([], maxlen)

    def avg (self):
        """returns average of list elements"""
        return sum(list(self)) / float(len(self))

    def last (self):
        """returns last list element"""
        return self[-1]

# eof #

