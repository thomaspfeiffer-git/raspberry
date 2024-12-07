# -*- coding: utf-8 -*-
############################################################################
# sound.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017, 2023, 2024    #
############################################################################

import subprocess

class Sound (object):
    """plays a sound
       - mp3: path to mp3 file
       - runs: how often the mp3 file shall be played
    """

    volume = 25

    @staticmethod
    def play (mp3, runs=1):
        # command = ["/usr/bin/mpg321", "-g 100", "-q"] + [mp3] * runs
        command = ["/usr/bin/cvlc", "--play-and-exit"] + [mp3] * runs
        process = subprocess.Popen(command)
        process.wait()
        process.communicate()

    @staticmethod
    def set_volume (volume:int):
        """sets the volume [percent]
           shell command: amixer -D pulse sset Master 50%
        """
        if not 0 <= volume <= 100:
            raise ValueError(f"volume is {volume}, must be in 0..100")

        Sound.volume = volume
        command = ["/usr/bin/amixer", "-D", "pulse", "sset", "Master", f"{volume}%"]
        process = subprocess.Popen(command)
        process.wait()
        process.communicate()

# eof #

