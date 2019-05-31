#!/usr/bin/env python3

import numpy as np

class Object:
    wall, none, mine, panel, check, opened = -1, 0, 9, 10, 11, 12

# objects
WALL, NONE = Object.wall, Object.none
MINE, PANEL, CHECK = Object.mine, Object.panel, Object.check

# win -> True
def check_win(board_data):
    status = board_data.status
    open_board = board_data.open_board
    closed_board = board_data.closed_board

    height = status.height
    width = status.width

    for i in range(height):
        for j in range(width):
            if closed_board[i+1][j+1] != MINE and open_board[i+1][j+1] not in range(0, 9):
                return False

    return True

# count_around
def count_around(board, value, i, j):
    counter = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            elif board[i+dx][j+dy] == value:
                counter += 1

    return counter

# remain_function
def counting_all(status, board, value):
    height = status.height
    width = status.width

    counter = 0
    for i in range(height):
        for j in range(width):
            if board[i+1][j+1] == value:
                counter += 1

    return counter

# remain_mine
def remain_mine(status, board):
    return status.mine - counting_all(status, board, CHECK)

class Status():
    def __init__(self, mine, height, width, time, state):
        self.mine = mine # the number of mines
        self.height = height # the height of board
        self.width = width # the width of board
        self.time = time # passed time in game
        self.state = state # True -> on game


class BoardData():
    def __init__(self, status):
        self.status = status # status object
        height = status.height
        width = status.width
        self.open_board = [[WALL for j in range(width+2)] for i in range(height+2)]
        self.closed_board = [[WALL for j in range(width+2)] for i in range(height+2)]

    # initialize_board
    def initialize(self):
        status = self.status
        open_board = self.open_board
        closed_board = self.closed_board

        mine = status.mine
        height = status.height
        width = status.width

        # remake open_board
        for i in range(height):
            for j in range(width):
                open_board[i+1][j+1] = PANEL

        # remake closed_board
        tmp_list = [NONE for i in range(height*width)]
        for i in range(mine):
            tmp_list[i] = MINE

        np.random.shuffle(tmp_list)
        for i in range(height):
            for j in range(width):
                closed_board[i+1][j+1] = tmp_list[width*i+j]

    # check_answer
    # # result == False -> show all mines, true -> check all mines
    def check_answer(self, result):
        status = self.status
        open_board = self.open_board
        closed_board = self.closed_board

        height = status.height
        width = status.width

        for i in range(height):
            for j in range(width):
                if result == False and closed_board[i+1][j+1] == MINE:
                    open_board[i+1][j+1] = MINE
                elif result == True and open_board[i+1][j+1] == PANEL and closed_board[i+1][j+1] == MINE:
                    open_board[i+1][j+1] = CHECK

    # open_panel
    def open_panel(self, i, j):
        status = self.status
        open_board = self.open_board
        closed_board = self.closed_board

        if open_board[i][j] != PANEL:
            pass
        else:
            if closed_board[i][j] == MINE:
                status.state = False
                self.check_answer(False)
            else:
                status.state = True
                open_board[i][j] = count_around(closed_board, MINE, i, j)
                if open_board[i][j] == 0:
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            if dx == 0 and dy == 0:
                                continue
                            self.open_panel(i+dx, j+dy)

            if check_win(self):
                status.state = False
                self.check_answer(True)

    # check_panel
    def check_panel(self, i, j):
        open_board = self.open_board
        if open_board[i][j] not in (PANEL, CHECK):
            pass
        else:
            open_board[i][j] = -open_board[i][j] + PANEL + CHECK
