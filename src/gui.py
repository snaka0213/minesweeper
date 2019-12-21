#!/usr/bin/env python3
import tkinter
import tkinter.simpledialog
from .board import Board
from .functions import argparser
from .objects import WALL, MINE, PANEL, CHECK, CONFIGS

class GUI(object):
    def __init__(self, b):
        self.b = b
        self.game_frame = None
        self.status_frame = None
        self.reset_root()

    def reset_root(self):
        self.root = tkinter.Tk()
        self.root.title("MineSweeper")

        self.root_frame = tkinter.Frame(
            self.root, **CONFIGS["root_frame"])

        self.reset_game()

    def reset_game(self):
        self.playing_time = 0

        if self.game_frame is not None:
            self.game_frame.destroy()

        self.game_frame = tkinter.Frame(
            self.root_frame, **CONFIGS["game_frame"])

        if self.status_frame is not None:
            self.status_frame.destroy()

        self.status_frame = tkinter.Frame(
            self.root_frame, **CONFIGS["game_frame"])

        self.root_frame.pack()
        self.status_frame.pack(pady=5, padx=5, fill='x')
        self.game_frame.pack(pady=5, padx=5)

        # button
        self.message_txt = tkinter.StringVar()
        self.message_txt.set("Solve")
        self.gui_message = tkinter.Label(self.status_frame,
            textvariable=self.message_txt, **CONFIGS["button"])

        self.gui_message.pack(fill='x')
        self.gui_message.bind("<Button-1>", lambda ev: self.solve())

        # remain mine
        self.remain_txt = tkinter.StringVar()
        self.remain_txt.set(str(self.b.remain_mine()))
        gui_remain = tkinter.Label(self.status_frame,
            textvariable=self.remain_txt, **CONFIGS["remain_mine"])

        gui_remain.pack(side='left')

        # timer
        self.timer_txt = tkinter.StringVar()
        self.timer_txt.set("{:0=3}".format(0))
        gui_timer = tkinter.Label(self.status_frame,
            textvariable=self.timer_txt, **CONFIGS["timer"])

        gui_timer.pack(side='right')

        self.reset_board()
        self.fit()

    """
    GUI board
    * left click: open panel
    * right click: (un)check panel
    """
    def reset_board(self):
        self.b.reset()
        H, W = self.b.height, self.b.width

        self.gui_board = [[WALL for j in range(W+2)] for i in range(H+2)]
        for i in range(1, H+1):
            for j in range(1, W+1):
                label = tkinter.Label(self.game_frame)
                label.coordinate = (i, j)
                label.config(**CONFIGS[PANEL])
                label.bind("<Button-1>", lambda ev: self.open_panel(
                    ev.widget.coordinate[0], ev.widget.coordinate[1]))
                label.bind("<Button-2>", lambda ev: self.check_panel(
                    ev.widget.coordinate[0], ev.widget.coordinate[1]))
                label.grid(row=i-1, column=j-1)
                self.gui_board[i][j] = label

    """
    end game
    """
    def end_game(self):
        H, W = self.b.height, self.b.width

        self.gui_message.unbind("<Button-1>")

        for i in range(1, H+1):
            for j in range(1, W+1):
                self.gui_board[i][j].unbind("<Button-1>")
                self.gui_board[i][j].unbind("<Button-2>")

        txt = "Game Clear!" if self.b.is_win() else "Game Over"
        self.message_txt.set(txt)

        self.sync_board()

    """
    open panel
    """
    def open_panel(self, i, j):
        if self.b.open_board[i][j] != PANEL:
            return

        if not self.b.is_playing:
            self.timer(start=True)

        self.b.open_panel(i, j, auto=False)
        value = self.b.open_board[i][j]
        self.gui_board[i][j].config(**CONFIGS[value])

        if value == MINE:
            self.end_game()
        elif value == 0:
            self.open_around(i, j)

        if self.b.is_win():
            self.end_game()

    """
    open around
    """
    def open_around(self, i, j):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                else:
                    self.open_panel(i+dx, j+dy)

    """
    (un)check panel
    """
    def check_panel(self, i, j):
        if not self.b.is_playing:
            self.timer(start=True)

        if self.b.open_board[i][j] == PANEL:
            self.b.check_panel(i, j)
        elif self.b.open_board[i][j] == CHECK:
            self.b.uncheck_panel(i, j)
        else:
            return

        value = self.b.open_board[i][j]
        self.gui_board[i][j].config(**CONFIGS[value])
        self.remain_txt.set(str(self.b.remain_mine()))

    """
    auto solver
    """
    def solve(self):
        self.b.solve()
        self.sync_board()
        if self.b.is_win():
            self.end_game()

    """
    sync gui_board with open_board
    """
    def sync_board(self):
        H, W = self.b.height, self.b.width
        for i in range(1, H+1):
            for j in range(1, W+1):
                value = self.b.open_board[i][j]
                self.gui_board[i][j].config(**CONFIGS[value])

        self.remain_txt.set(str(self.b.remain_mine()))

    """
    timer
    """
    def timer(self, start=False):
        if not (self.b.is_playing or start) or self.b.is_win():
            pass
        else:
            self.root.after(1000, self.timer)
            txt = "{:0=3}".format(self.playing_time)
            self.timer_txt.set(txt)
            self.playing_time += 1

    """
    fit window
    * centering(bool): also centering window or not
    """
    def fit(self, centering=True):
        self.root.update_idletasks()
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        self.root.geometry('{}x{}'.format(window_width, window_height))

        if centering:
            x = self.root.winfo_screenwidth() // 2 - window_width // 2
            y = self.root.winfo_screenheight() // 2 - window_height // 2
            self.root.geometry('+{}+{}'.format(x, y))

        self.root.deiconify()

    """
    root main loop
    """
    def loop(self):
        self.root.mainloop()
