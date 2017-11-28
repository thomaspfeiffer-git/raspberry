# -*- coding: utf-8 -*-
############################################################################
# Commons.py                                                               ä
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""

Usage:
    class X (metaclass=Singleton):
        pass
"""

class Singleton (type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# eof #

