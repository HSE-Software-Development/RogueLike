from __future__ import annotations
from pydantic import BaseModel
from enum import Enum
import curses


class Color(Enum):
    RED = (1, curses.COLOR_RED, curses.COLOR_BLACK)
    GREEN = (2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    YELLOW = (3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    BLUE = (4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    PURPLE = (5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    CYAN = (6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    WHITE = (7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    BLACK_WHITE = (8, curses.COLOR_BLACK, curses.COLOR_WHITE)
    BLACK_YELLOW = (9, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    BLACK_RED = (10, curses.COLOR_BLACK, curses.COLOR_RED)
    BLACK_GREEN = (11, curses.COLOR_BLACK, curses.COLOR_GREEN)


class Effect(Enum):
    BOLD = curses.A_BOLD
    ITALIC = curses.A_ITALIC
    DIM = curses.A_DIM
    BLINK = curses.A_BLINK
    UNDERLINE = curses.A_UNDERLINE


class Cell:

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __add__(self, other: Cell):
        return Cell(
            x=self.x + other.x,
            y=self.y + other.y,
        )

    def __iadd__(self, other: Cell):
        self.x += other.x
        self.y += other.y

    def __sub__(self, other: Cell):
        return Cell(
            x=self.x - other.x,
            y=self.y - other.y,
        )

    def __isub__(self, other: Cell):
        self.x -= other.x
        self.y -= other.y

    def distance(self, other: Cell) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def is_inside(self, p0: Cell, p1: Cell):
        min_x = min(p0.x, p1.x)
        max_x = max(p0.x, p1.x)
        min_y = min(p0.y, p1.y)
        max_y = max(p0.y, p1.y)

        return min_x < self.x < max_x and min_y < self.y < max_y

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Rect:
    def __init__(self, lt: Cell, rb: Cell):
        self.lt = lt
        self.rb = rb

    @property
    def left(self) -> int:
        return self.lt.x

    @property
    def right(self) -> int:
        return self.rb.x

    @property
    def top(self) -> int:
        return self.lt.y

    @property
    def bottom(self) -> int:
        return self.rb.y

    @property
    def width(self) -> int:
        return self.rb.x - self.lt.x + 1

    @property
    def height(self) -> int:
        return self.rb.y - self.lt.y + 1

    def is_inside(self, cell: Cell):
        return cell.is_inside(self.lt, self.rb)

    def is_outside(self, cell: Cell):
        return (
            cell.x < self.left
            or cell.x > self.right
            or cell.y < self.top
            or cell.y > self.bottom
        )

    def is_on_edge(self, cell: Cell):
        return (
            (cell.x == self.left or cell.x == self.right)
            and self.top <= cell.y <= self.bottom
            or (cell.y == self.top or cell.y == self.bottom)
            and self.left <= cell.x <= self.right
        )

    def is_intersect(self, other: Rect) -> bool:
        return not (
            self.left > other.right
            or self.right < other.left
            or self.top > other.bottom
            or self.bottom < other.top
        )

    def with_margin(self, margin: int) -> Rect:
        return Rect(
            Cell(self.lt.x - margin, self.lt.y - margin),
            Cell(self.rb.x + margin, self.rb.y + margin),
        )

    @property
    def center(self) -> Cell:
        return Cell(
            x=(self.lt.x + self.rb.x) // 2,
            y=(self.lt.y + self.rb.y) // 2,
        )

    def __str__(self):
        return f"Rect(lt=({self.lt.x}, {self.lt.y}), rb=({self.rb.x}, {self.rb.y}))"
