#!/usr/bin/env python3
"""
objects in MineSweeper
* WALL: edge of the squared board
* MINE: mine in the board
* PANEL: panel which is not opened in board
* CHECK: one use this when they suspect mine
* OPEND: cpu use this when it solve virtual board
* OBJECTS: used in CLI
* CONFIGS: used in GUI
"""
WALL   = -1
MINE   = 9
PANEL  = 10
CHECK  = 11
OPENED = 12
OBJECTS = ['　', '１', '２', '３', '４', '５', '６', '７', '８', '＊', '・', '＃']
CONFIGS = {
    0: {"relief": "ridge", "bg": "LightGray"},
    1: {"relief": "ridge", "bg": "LightGray", "fg": "Blue", "text": "１"},
    2: {"relief": "ridge", "bg": "LightGray", "fg": "Green", "text": "２"},
    3: {"relief": "ridge", "bg": "LightGray", "fg": "Red", "text": "３"},
    4: {"relief": "ridge", "bg": "LightGray", "fg": "Purple", "text": "４"},
    5: {"relief": "ridge", "bg": "LightGray", "fg": "Maroon", "text": "５"},
    6: {"relief": "ridge", "bg": "LightGray", "fg": "Turquoise", "text": "６"},
    7: {"relief": "ridge", "bg": "LightGray", "fg": "Black", "text": "７"},
    8: {"relief": "ridge", "bg": "LightGray", "fg": "Gray", "text": "８"},
    MINE: {"relief": "ridge", "bg": "Red", "fg": "Black", "text": "＊"},
    PANEL: {"relief": "raised", "height": 1, "width": 2, "bd": 2, "bg": "LightGray", "text": "　"},
    CHECK: {"relief": "raised", "bg": "LightGray", "fg": "Black", "text": "＃"},
    "root_frame": {"relief": "ridge", "bg": "LightGray"},
    "game_frame": {"relief": "sunken", "bd": 3, "bg": "LightGray"},
    "button": {"relief": "raised",  "bd": 2, "bg": "LightGray"},
    "remain_mine": {"width": 5, "bg": "LightGray"},
    "timer": {"width": 5, "bg": "LightGray"},
}
