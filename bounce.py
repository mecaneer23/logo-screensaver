#!/usr/bin/env python3
"""
Animate a logo bouncing around a screen
"""

import curses
import sys
from enum import Enum
from pathlib import Path
from random import choice


class Color(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7

    def as_int(self) -> int:
        """
        Returns the color pair value corresponding to the color
        """
        return self.value

    @staticmethod
    def values() -> list[int]:
        """
        Returns a list of all color values
        """
        return [color.value for color in Color]

class BouncingLogo:
    def __init__(self, filename: Path, stdscr: curses.window) -> None:
        self._stdscr = stdscr
        with filename.open("r") as file:
            self._text = file.read().splitlines()
        self._width = len(max(self._text, key=len))
        self._height = len(self._text)
        self._x = 0
        self._y = 0
        self._x_vel = 2
        self._y_vel = 1
        self._color = curses.color_pair(Color.WHITE.as_int())
        self._stdscr.nodelay(True)  # noqa: FBT003

    def _display(self, y: int, x: int) -> None:
        self._stdscr.clear()
        for row_index, line in enumerate(self._text):
            self._stdscr.addstr(y + row_index, x, line, self._color)
        self._stdscr.refresh()

    def _move(self) -> None:
        self._check_collision()
        self._x += self._x_vel
        self._y += self._y_vel

    def _update_color(self, color: int) -> None:
        self._color = curses.color_pair(color)

    def _check_collision(self) -> None:
        lines, cols = self._stdscr.getmaxyx()
        # TODO: why do we have to subtract 1 from cols when _x_vel is 2?
        if (self._x <= 0 and self._x_vel < 0) or (
            self._x + self._width >= cols - 1 and self._x_vel > 0
        ):
            self._x_vel *= -1
            self._update_color(choice(Color.values()))  # noqa: S311
        if (self._y <= 0 and self._y_vel < 0) or (
            self._y >= lines - self._height and self._y_vel > 0
        ):
            self._y_vel *= -1
            self._update_color(choice(Color.values()))  # noqa: S311

    def start(self) -> None:
        while True:
            self._display(self._y, self._x)
            self._move()
            curses.napms(100)
            if self._stdscr.getch() != -1:
                break


def _init() -> None:
    curses.use_default_colors()
    curses.curs_set(0)
    for i, color in enumerate(
        (
            curses.COLOR_RED,
            curses.COLOR_GREEN,
            curses.COLOR_YELLOW,
            curses.COLOR_BLUE,
            curses.COLOR_MAGENTA,
            curses.COLOR_CYAN,
            curses.COLOR_WHITE,
        ),
        start=1,
    ):
        curses.init_pair(i, color, -1)


def main(stdscr: curses.window) -> int:
    _init()
    animation = BouncingLogo(Path("logo.txt"), stdscr)
    try:
        animation.start()
    except KeyboardInterrupt:
        return 0
    return -1


if __name__ == "__main__":
    sys.exit(curses.wrapper(main))
