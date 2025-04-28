#!/usr/bin/env python3
"""
Animate a logo bouncing around a screen
"""

import curses
import sys


def main(stdscr: curses.window) -> int:
    return 0


if __name__ == "__main__":
    sys.exit(curses.wrapper(main))
