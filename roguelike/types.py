from __future__ import annotations
from pydantic import BaseModel
from enum import Enum


class Color(Enum):
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37


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
        return self.rb.x - self.lt.x

    @property
    def height(self) -> int:
        return self.rb.y - self.lt.y

    def is_inside(self, cell: Cell):
        return cell.is_inside(self.lt, self.rb)

    def is_intersect(self, other: Rect):
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
