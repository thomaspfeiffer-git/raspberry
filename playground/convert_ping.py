#!/usr/bin/python3 -u

from datetime import datetime
import sys

sys.stdin.readline() # ignore first line
for line in sys.stdin:
    line = line.split(" ")
    line[0] = "{}: ".format(datetime.fromtimestamp(float(line[0].strip('[').rstrip(']'))))
    print(" ".join(line), end="")


