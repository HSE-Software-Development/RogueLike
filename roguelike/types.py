from __future__ import annotations


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
        self.x -= (other.x,)
        self.y -= (other.y,)
