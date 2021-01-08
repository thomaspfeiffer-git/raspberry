# -*- coding: utf-8 -*-
############################################################################
# sound.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################

import subprocess

class Sound (object):
    """plays a sound
       - mp3: path to mp3 file
       - runs: how often the mp3 file shall be played
    """
    @staticmethod
    def play (mp3, runs=1):
        command = ["mpg321", "-g 100", "-q"] + [mp3] * runs
        process = subprocess.Popen(command)
        process.wait()
        process.communicate()

# eof #

