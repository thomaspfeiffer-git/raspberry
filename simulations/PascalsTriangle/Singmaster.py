#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Singmaster.py                                                               #
# (c) https://github.com/thomaspfeiffer-git 2022                              #
###############################################################################
"""
https://en.wikipedia.org/wiki/Singmaster%27s_conjecture

"""

from collections import defaultdict

iterations = 10000
max_appaerances = 50

def pascal (line):
    next_line = []
    for i in range(len(line)-1):
        next_line.append(line[i] + line[i+1])
    next_line.insert(0, 0)
    next_line.append(0)
    return next_line


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    line = [0, 1, 0]
    count = defaultdict(int)
    appearances = defaultdict(list)

    for i in range(iterations):
        line = pascal(line)
        for number in line:
            if count[number] < max_appaerances:
                count[number] += 1

    for number in count.keys():
        appearances[count[number]].append(number)

    for i in appearances:
        if len(appearances[i]) >= max_appaerances:
            print(f"{i}: [more than {max_appaerances} items]")
        else:
            appearances[i].sort()
            print(f"{i}: {appearances[i]}")


