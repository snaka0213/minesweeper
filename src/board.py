#!/usr/bin/env python3
import sys
import copy
import time
import random
import itertools
from .functions import argparser, count_around, v_direct_solver, is_solvable_panel, is_reasonable
from .objects import WALL, MINE, PANEL, CHECK, OPENED, OBJECTS

class Board(object):
    """
    * mine (int): the number of mines in board
    * height, width (int): the size of squared board
    * init_i, init_j (int): the coordinates of initial panel
    """
    def __init__(self, *, mine, height, width, init_i=1, init_j=1):
        if mine >= height*width:
            raise ValueError("the number of mine ({}) must be less than "\
            "the size of board ({}*{})".format(mine, height, width))

        self.mine   = mine
        self.height = height
        self.width  = width
        self.reset(init_i, init_j)

    """
    (re)inirialize board
    * we build closed_board to hold board[init_i][init_j] != MINE
    * n_check (int): the number of check in open_board
    * start_time (time): game start time
    * is_playing (bool): True when the game playing
    """
    def reset(self, init_i=1, init_j=1):
        self.n_check    = 0
        self.start_time = time.time()
        self.is_playing = False

        M, H, W = self.mine, self.height, self.width

        self.open_board = [[WALL for j in range(W+2)] for i in range(H+2)]
        self.closed_board = [[WALL for j in range(W+2)] for i in range(H+2)]

        # initialize open_board
        for i in range(1, H+1):
            for j in range(1, W+1):
                self.open_board[i][j] = PANEL

        # initialize closed_board
        _i, _j = list(range(1, H+1)), list(range(1, W+1))
        coordinates = list(itertools.product(_i, _j))
        coordinates.remove((init_i, init_j))
        mine_coordinates = set(random.sample(coordinates, M))
        for i in range(1, H+1):
            for j in range(1, W+1):
                self.closed_board[i][j] =\
                MINE if (i, j) in mine_coordinates else 0

    """
    check answer - show all mines
    (that is, make each PANEL to be MINE)
    """
    def check_answer(self):
        H, W = self.height, self.width

        for i in range(1, H+1):
            for j in range(1, W+1):
                self._sync_mine(i, j)

    def _sync_mine(self, i, j):
        if self.closed_board[i][j] == MINE:
            self.open_board[i][j] = MINE

    """
    fill check - fill check in open_board
    """
    def fill_check(self):
        H, W = self.height, self.width

        for i in range(1, H+1):
            for j in range(1, W+1):
                self._sync_check(i, j)

    def _sync_check(self, i, j):
        if self.open_board[i][j] == PANEL and self.closed_board[i][j] == MINE:
            self.open_board[i][j] = CHECK
            self.n_check += 1

    """
    open panel
    * auto (bool): open automatically zero panel or not
    """
    def open_panel(self, i, j, auto=True):
        if not self.is_playing:
            self.is_playing = True
            self.reset(i, j)

        if self.open_board[i][j] != PANEL:
            pass
        elif self.closed_board[i][j] == MINE:
            self.is_playing = False
            self.check_answer()
        else:
            self.is_playing = True
            self.open_board[i][j] = count_around(self.closed_board, MINE, i, j)
            if auto and self.open_board[i][j] == 0:
                self.open_around(i, j, auto)

        if self.is_win():
            self.fill_check()

    """
    open around
    """
    def open_around(self, i, j, auto=True):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                else:
                    self.open_panel(i+dx, j+dy, auto)

    """
    check panel
    """
    def check_panel(self, i, j):
        if not self.is_playing:
            self.is_playing = True
            
        if self.open_board[i][j] == PANEL:
            self.open_board[i][j] = CHECK
            self.n_check += 1
        else:
            pass

    """
    uncheck panel
    """
    def uncheck_panel(self, i, j):
        if self.open_board[i][j] == CHECK:
            self.open_board[i][j] = PANEL
            self.n_check -= 1
        else:
            pass

    """
    check around
    """
    def check_around(self, i, j):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                else:
                    self.check_panel(i+dx, j+dy)

    """
    win -> True
    """
    def is_win(self):
        H, W = self.height, self.width

        for i in range(1, H+1):
            for j in range(1, W+1):
                if self.closed_board[i][j] != MINE and\
                    self.open_board[i][j] not in range(0, 9):
                    return False

        return True

    """
    return #MINE - #CHECK in open_board
    """
    def remain_mine(self):
        return self.mine - self.n_check

    """
    return time.time() - start_time
    """
    def playing_time(self):
        if self.start_time is None:
            return 0.0

        return time.time() - self.start_time

    """
    show open_board in console line
    """
    def show_board(self):
        H, W = self.height, self.width

        print("＝"*W)

        for i in range(1, H+1):
            line = ''
            for j in range(1, W+1):
                line += OBJECTS[self.open_board[i][j]]
            print(line)

        print("＝"*W)

    """
    direct solver - open or check around panel as many as possible:
    change each panel which satisfies some of the following conditions:
    * #CHECK in around == open_board[i][j] -> open around.
    * #CHECK + #PANEL in around == open_board[i][j] -> check around.
    """
    def solve_direct(self):
        H, W = self.height, self.width

        SIZE = H*W
        counter = 0
        while counter != SIZE:
            counter = 0
            for i in range(1, H+1):
                for j in range(1, W+1):
                    if is_solvable_panel(self.open_board, i, j):
                        p = count_around(self.open_board, PANEL, i, j)
                        c = count_around(self.open_board, CHECK, i, j)
                        if self.open_board[i][j] == c:
                            self.open_around(i, j)
                        elif self.open_board[i][j] == c+p:
                            self.check_around(i, j)
                        else:
                            counter += 1
                    else:
                        counter += 1

    """
    indirect solver - open panel by contradiction:
    one put a virtual mine on a panel,
    and if board conditions contradict, then open the panel.
    """
    def solve_indirect(self):
        H, W = self.height, self.width
        SIZE = H*W

        counter = 0
        while counter != SIZE:
            counter = 0
            for i in range(1, H+1):
                for j in range(1, W+1):
                    if self.open_board[i][j] == PANEL:
                        _board = copy.deepcopy(self.open_board)
                        _board[i][j] = CHECK
                        v_direct_solver(_board, 1, H+1, 1, W+1)
                        if not is_reasonable(_board, 1, H+1, 1, W+1):
                            self.open_panel(i, j)
                            self.solve_direct()
                        else:
                            counter += 1
                    else:
                        counter += 1

    """
    auto solver
    """
    def solve(self):
        self.solve_direct()
        self.solve_indirect()

def main(args):
    b = Board(mine=args.mine, height=args.height, width=args.width)

    while not b.is_win():
        b.show_board()
        select = input("open / check / solve / exit >> ")
        if select == "exit":
            print("Game exited.")
            sys.exit()
        elif select == "solve":
            b.solve()
            continue

        elif select not in {"open", "check"}:
            print("UserError: undefined control.")
            continue

        i = int(input("column >> "))
        j = int(input("row >> "))

        if not (i in range(1, b.height+1) and j in range(1, b.width+1)):
            print("UserError: the coordinate is out of range.")
            continue

        if select == "open":
            b.open_panel(i, j)
            if b.open_board[i][j] == MINE:
                b.show_board()
                print("Game Over")
                sys.exit()
        elif select == "check":
            if b.open_board[i][j] == PANEL:
                b.check_panel(i, j)
            elif b.open_board[i][j] == CHECK:
                b.uncheck_panel(i, j)

    b.show_board()
    print("Game Clear!")
    print("Clear Time: {t:.2f}s".format(t=b.playing_time()))
    sys.exit()

if __name__ == "__main__":
    args = argparser()
    main(args)
