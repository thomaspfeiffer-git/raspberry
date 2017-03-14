#!/usr/bin/python3
###############################################################################
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################

import math
from random import random

a, b, iterations = 0, 0, 10000000

for i in range(iterations):
    if math.sqrt(random()**2.0 + random()**2.0) < 1.0:
        a += 1
    else:
        b += 1

mypi = 4.0*a/iterations
print("mypi: {:.50g}".format(mypi))
print("accuracy: {:2.10g} %".format((math.pi-mypi)/math.pi))



# eof #

