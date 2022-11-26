#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# IsPrime.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2022                              #
###############################################################################

"""
some playing around with isPrime() and performance optimizations
"""

import math
import sympy
import time

max = 1000000

def isPrime_lowPerf (n):
    if n <= 1: return False
    for i in range(2,n):
        if n % i == 0:
            return False
    return True


def isPrime_highPerf (n):
    if n <= 1: return False
    if n == 2 or n == 3 or n == 5 or n == 7: return True
    if n % 2 == 0: return False
    if n % 3 == 0: return False
    if n % 5 == 0: return False
    if n % 7 == 0: return False
    for i in range(11, int(math.sqrt(n)), 2):
        if (n % i == 0):
            return False
    return True


def test (algorithm):
    start = time.time()
    for i in range(max):
        if algorithm(i):
            None
    end = time.time()
    return end - start


print(f"Low performance execution time: {test(isPrime_lowPerf):.2f}")
print(f"High performance execution time: {test(isPrime_highPerf):.2f}")
print(f"Very high performance execution time: {test(sympy.isprime):.2f}")

# eof #

