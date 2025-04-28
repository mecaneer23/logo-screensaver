#!/usr/bin/env python3
"""
Animate a logo bouncing around a screen
"""

import curses
import sys
from pathlib import Path


class BouncingLogo:
    def __init__(self, filename: Path, stdscr: curses.window) -> None:
        curses.curs_set(0)
        self._stdscr = stdscr
        with filename.open("r") as file:
            self._text = file.read().splitlines()
        self._width = len(max(self._text, key=len))
        self._height = len(self._text)
        self._x = 0
        self._y = 0
        self._x_vel = 1
        self._y_vel = 1

    def _display(self, y: int, x: int) -> None:
        self._stdscr.clear()
        for row_index, line in enumerate(self._text):
            self._stdscr.addstr(y + row_index, x, line)
        self._stdscr.refresh()

    def _move(self) -> None:
        self._check_collision()
        self._x += self._x_vel
        self._y += self._y_vel

    def _check_collision(self) -> None:
        lines, cols = self._stdscr.getmaxyx()
        if (self._x <= 0 and self._x_vel < 0) or (
            self._x >= cols - self._width and self._x_vel > 0
        ):
            self._x_vel *= -1
        if (self._y <= 0 and self._y_vel < 0) or (
            self._y >= lines - self._height and self._y_vel > 0
        ):
            self._y_vel *= -1

    def start(self) -> None:
        while True:
            self._display(self._y, self._x)
            self._move()
            curses.napms(100)


def main(stdscr: curses.window) -> int:
    BouncingLogo(Path("logo.txt"), stdscr).start()
    return 0


if __name__ == "__main__":
    sys.exit(curses.wrapper(main))
