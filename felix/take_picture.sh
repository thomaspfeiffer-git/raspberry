#!/bin/bash


export LIB....

# -r 2592x1944

mjpg_streamer -i input_uvc.so -d /dev/video0 -r 1280x960 -f 1 -q 95 \
              -o output_file.so -d 15 -c ./blink.sh



