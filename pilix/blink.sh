#!/bin/bash
# blink.sh:
# blinks a LED attached to pin $Param
# called by the -c param of mjpg-streamer plugin output_file.so
# precondition: pin has to be switched to output
# (c) Thomas Pfeiffer, 2017

gpio -1 write $1 1
gpio -1 write $1 0

# eof #

