#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Sudoku.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2024                              #
###############################################################################

"""
https://mathe-gut-erklaert.de/pdfs/000_Sudoku.pdf
"""

board = [0, 0, 0,  0, 0, 0,  0, 0, 8,   #  0 ..  8
         0, 2, 0,  0, 5, 0,  7, 6, 0,   #  9 .. 17
         0, 6, 0,  0, 0, 0,  0, 0, 3,   # 18 .. 26

         5, 0, 0,  0, 0, 0,  2, 0, 7,   # 27 .. 35
         0, 3, 0,  0, 1, 0,  0, 0, 0,   # 36 .. 44
         2, 0, 0,  4, 0, 0,  0, 3, 0,   # 45 .. 53

         0, 0, 0,  6, 0, 0,  0, 0, 0,   # 54 .. 62
         8, 0, 0,  0, 0, 0,  0, 0, 0,   # 63 .. 71
         1, 0, 0,  2, 7, 0,  0, 4, 0]   # 72 .. 80

from collections import Counter
import sys
sys.path.append("../libs/")
from Logging import Log


###############################################################################
# getRowCol ###################################################################
def getColRow (index):
    return (index % 9, index // 9)

def getCol (index):
    return getColRow(index)[0]

def getRow (index):
    return getColRow(index)[1]


###############################################################################
# allowedDigits ###############################################################
def allowedDigitsRow (index):
    allowed = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    row = getRow(index)
    for i in range(9):
        if board[row*9+i] in allowed:
            allowed.remove(board[row*9+i])
    return allowed

def allowedDigitsCol (index):
    allowed = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    col = getCol(index)
    for i in range(9):
        if board[col+i*9] in allowed:
            allowed.remove(board[col+i*9])
    return allowed

def allowedDigitsBox (index):
    allowed = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    box_x = getCol(i) // 3 * 3    # left upper corner in box
    box_y = getRow(i) // 3 * 3

    for y in range(box_y, box_y+3):
        for x in range(y*9 + box_x, y*9 + box_x+3):
            if board[x] in allowed:
                allowed.remove(board[x])
    return allowed

def allowedDigits (index):
    allowed = []
    for digit, count in dict(Counter(allowedDigitsRow(i) + allowedDigitsCol(i) + allowedDigitsBox(i))).items():
        if count == 3:
            allowed.append(digit)

    return allowed


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    i = 0
    Log(allowedDigits(i))

# eof #

