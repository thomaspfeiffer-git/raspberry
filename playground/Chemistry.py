#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Chemistry.py                                                                #
# (c) https://github.com/thomaspfeiffer-git 2024                              #
###############################################################################
"""
"""

import re


molecule = "2 Na2Cl2OH"

items = re.findall(r'\d*|[A-Z][a-z]?', molecule)
print(items)

elements = {}
quantifier = None

for i, item in enumerate(items):
    if item == '':
        continue
    if quantifier is None:
        if re.fullmatch(r'\d+', item):
            quantifier = int(item)
        else:
            quantifier = 1

    if re.fullmatch(r'[A-Z][a-z]?', item):
        element = item
        count = 1
        if re.fullmatch(r'\d+', items[i+1]):
            count = int(items[i+1])
        elements[element] = quantifier * count

print(elements)


# eof #

