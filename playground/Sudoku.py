#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Sudoku.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2024                              #
###############################################################################

"""
https://mathe-gut-erklaert.de/pdfs/000_Sudoku.pdf
"""

board1 = [0, 0, 0,  0, 0, 0,  0, 0, 8,   #  0 ..  8
          0, 2, 0,  0, 5, 0,  7, 6, 0,   #  9 .. 17
          0, 6, 0,  0, 0, 0,  0, 0, 3,   # 18 .. 26

          5, 0, 0,  0, 0, 0,  2, 0, 7,   # 27 .. 35
          0, 3, 0,  0, 1, 0,  0, 0, 0,   # 36 .. 44
          2, 0, 0,  4, 0, 0,  0, 3, 0,   # 45 .. 53

          0, 0, 0,  6, 0, 0,  0, 0, 0,   # 54 .. 62
          8, 0, 0,  0, 0, 0,  0, 0, 0,   # 63 .. 71
          1, 0, 0,  2, 7, 0,  0, 4, 0]   # 72 .. 80

board2 = [3, 0, 6, 5, 0, 8, 4, 0, 0,
          5, 2, 0, 0, 0, 0, 0, 0, 0,
          0, 8, 7, 0, 0, 0, 0, 3, 1,
          0, 0, 3, 0, 1, 0, 0, 8, 0,
          9, 0, 0, 8, 6, 3, 0, 0, 5,
          0, 5, 0, 0, 9, 0, 6, 0, 0,
          1, 3, 0, 0, 0, 0, 2, 5, 0,
          0, 0, 0, 0, 0, 0, 0, 7, 4,
          0, 0, 5, 2, 0, 6, 3, 0, 0]

board = board1

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
    box_x = getCol(index) // 3 * 3    # left upper corner in box
    box_y = getRow(index) // 3 * 3

    for y in range(box_y, box_y+3):
        for x in range(y*9 + box_x, y*9 + box_x+3):
            if board[x] in allowed:
                allowed.remove(board[x])
    return allowed

def allowedDigits (index):
    allowed = []
    for digit, count in dict(Counter(allowedDigitsRow(index) +
                                     allowedDigitsCol(index) +
                                     allowedDigitsBox(index))).items():
        if count == 3:
            allowed.append(digit)
    return allowed


###############################################################################
# solve #######################################################################
def solve (index):
    DONE = 1
    END_PATH = 2

    def nextFreeCell (index):
        for i in range(81):
            if board[i] == 0:
                return i
        return None

    index = nextFreeCell(index)
    if index is None:
        return DONE

    allowed = allowedDigits(index)
    if len(allowed) == 0:
        return END_PATH

    for i in allowed:
        board[index] = i
        if solve(index) == DONE:
            return DONE
        board[index] = 0

    return END_PATH


###############################################################################
# printBoard ##################################################################
def printBoard (board):
    for line in range(9):
        print(f"{board[line*9:line*9+3]} {board[line*9+3:line*9+6]} {board[line*9+6:line*9+9]}")
        if (line+1) % 3 == 0:
            print()


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    solve(0)
    printBoard(board)

# eof #

