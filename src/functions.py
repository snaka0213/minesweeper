#!/usr/bin/env python3
import argparse
from .objects import WALL, MINE, PANEL, CHECK, OPENED

"""
argument parser
"""
def argparser(mine=40, height=16, width=16):
    parser = argparse.ArgumentParser()

    # board settings
    parser.add_argument("--mine", type=int, default=mine)
    parser.add_argument("--height", type=int, default=height)
    parser.add_argument("--width", type=int, default=width)

    args = parser.parse_args()
    return args

"""
count #object around of board[i][j].
* board: 2-dim list
"""
def count_around(board, object, i, j):
    counter = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            elif board[i+dx][j+dy] == object:
                counter += 1

    return counter

"""
change all PANEL around of board[i][j] to object.
"""
def change_around(board, object, i, j):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            elif board[i+dx][j+dy] == PANEL:
                board[i+dx][j+dy] = object

"""
virtual direct solver - virtualy open panels as many as possible:
change each panel which satisfies some of the following conditions:
* #CHECK in around == board[i][j] -> open around.
* #CHECK + #PANEL in around == board[i][j] -> check around.
"""
def v_direct_solver(board, start_h, end_h, start_w, end_w):
    SIZE = (end_h-start_h)*(end_w-start_w)

    counter = 0
    while counter != SIZE:
        counter = 0
        for i in range(start_h, end_h):
            for j in range(start_w, end_w):
                if is_solvable_panel(board, i, j):
                    p = count_around(board, PANEL, i, j)
                    c = count_around(board, CHECK, i, j)
                    if board[i][j] == c:
                        change_around(board, OPENED, i, j)
                    elif board[i][j] == c+p:
                        change_around(board, CHECK, i, j)
                    else:
                        counter += 1
                else:
                    counter += 1

"""
return True iff the following conditions hold:
* board[i][j] is a number panel (in range(1, 9))
* #PANEL in around > 0
"""
def is_solvable_panel(board, i, j):
    return board[i][j] in range(1, 9) and\
        count_around(board, PANEL, i, j) > 0

"""
return True if board does not contradict.
"""
def is_reasonable(board, start_h, end_h, start_w, end_w):
    for i in range(start_h, end_h):
        for j in range(start_w, end_w):
            if board[i][j] not in range(1, 9):
                continue
            elif board[i][j] < count_around(board, CHECK, i, j):
                return False
    else:
        return True
