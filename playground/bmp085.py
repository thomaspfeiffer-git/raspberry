#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys

sys.path.append('../libs')
sys.path.append('../libs/sensors')

import BMP085


b = BMP085.BMP085()
print "Druck: %s" % b.read()


