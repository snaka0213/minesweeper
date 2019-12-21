#!/usr/bin/env python3
from src.functions import argparser
from src.board import Board
from src.gui import GUI

def main(args):
    b = Board(mine=args.mine, height=args.height, width=args.width)
    gui = GUI(b)
    gui.loop()

if __name__ == "__main__":
    args = argparser()
    main(args)
