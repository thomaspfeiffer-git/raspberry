#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Sandpiles.py                                                                #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                   #
###############################################################################
"""
Some playground for the sandpile model.
https://en.wikipedia.org/wiki/Abelian_sandpile_model
"""

### Usage ###
# ./Sandpiles.py 

### you might need to install ###
# sudo pip3 install Pillow


import copy
import json
import multiprocessing
import sys
import time

from Config import CONFIG, filename
from Logging import Log
from Shutdown import Shutdown


###############################################################################
# Pile ########################################################################
class Pile (object):
    def __init__ (self, grains=CONFIG.PILE.GRAINS):
        self.pile = [[0 for x in range(CONFIG.PILE.X)] for y in range(CONFIG.PILE.Y)]
        self.pile[CONFIG.PILE.X//2][CONFIG.PILE.Y//2] = grains

    def save (self):
        with open(filename("sp"), 'w') as f:
            json.dump(self.pile, f, separators=(',', ':'))

    def share (self):
        if do_draw.value == 0: # update only if last update was consumed
            do_draw.value = 1
            for x in range(CONFIG.PILE.X):
                for y in range(CONFIG.PILE.Y):
                    shared_pile[self.pindex(x,y)] = self.pile[x][y]

    def localize (self):
        for x in range(CONFIG.PILE.X):
            for y in range(CONFIG.PILE.Y):
                self.pile[x][y] = shared_pile[self.pindex(x,y)]

    @staticmethod
    def pindex (x, y):
        return x + CONFIG.PILE.X * y


###############################################################################
# Calculate ###################################################################
class Calculate (object):
    def __init__ (self):
        pass

    def iterate (self):
        """ algorithm taken from
            https://en.wikipedia.org/wiki/Abelian_sandpile_model#Definition
            The final configuration does not depend on the chosen order.
        """    
        toppled = 0
        for x in range(CONFIG.PILE.X):
            for y in range(CONFIG.PILE.Y):
                if pile.pile[x][y] >= CONFIG.PILE.MAX_GRAINS_PER_FIELD:  # topple
                    pile.pile[x][y] -= CONFIG.PILE.MAX_GRAINS_PER_FIELD
                    try:
                        pile.pile[x-1][y] += 1
                        pile.pile[x+1][y] += 1
                        pile.pile[x][y-1] += 1
                        pile.pile[x][y+1] += 1
                    except IndexError:
                        pass  # grains disappear at the edge of the field
                    toppled += 1

        return toppled

    def run (self):
        def share_and_log ():
            pile.save()
            pile.share()
            Log("Iteration #{}: {} field(s) toppled; grains on center field: {}"
                .format(i, toppled, pile.pile[CONFIG.PILE.X//2][CONFIG.PILE.Y//2]))

        i = 0
        toppled = None
        while toppled != 0:
            toppled = self.iterate()
            i += 1
            if i % 2500 == 0:
                share_and_log()
              
        Log("Done!")
        share_and_log()


###############################################################################
# shutdown_application ########################################################
def shutdown_application ():
    """called on shutdown; stops all threads"""
    Log("shutdown_application()")
    # TODO: Check if call to stop(), exit(), join() or similar necessary
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    shared_pile = multiprocessing.Array('i', [0 for i in range(CONFIG.PILE.X * CONFIG.PILE.Y)], lock=False)
    do_draw = multiprocessing.Value('i', 0)
    pile = Pile()

    calculate = Calculate()
    p = multiprocessing.Process(target=calculate.run, args=())
    p.start()

    """
    Parameters:
    --calculate [ --display ]
    --displayfromfiles=<pattern>

    """


    import os
    import Display
    try:
        os.environ["DISPLAY"]
    except KeyError:
        Log("$DISPLAY not set, using default :0.0")
        os.environ["DISPLAY"] = ":0.0"


    tk_app = Display.TkApp(pile, do_draw)
    tk_app.run()

    p.join()

# eof #

