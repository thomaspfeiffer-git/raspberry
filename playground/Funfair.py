#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Funfair.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2022                              #
###############################################################################


iterations = 10
rounds = 1000000


red = 0
blue = 1
box = [red, blue] * 10

def draw(box):
    from random import randrange

    index = randrange(len(box))
    item = box[index]
    del box[index]
    return item

for i in range(iterations):
    stake = 0
    wins  = 0

    for _ in range(rounds):
        current_box = box.copy()
        stake += 2

        for _ in range(3):
            if draw(current_box) == blue:
                break
        else:
            wins += 1

    print(f"Iteration: {i}: stakes: {stake}; wins: {wins}; ratio: {stake/wins:.2f}")

# eof #

