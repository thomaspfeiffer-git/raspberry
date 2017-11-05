#!/bin/bash


export LIB....

./mjpg_streamer -i "input_uvc.so -y 1 -f 1 -r 2592x1936 -q 95 -n" \
              -o "output_file.so -d 15000"



