from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import threading
import uuid
import time
import os
import curses


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


class GameObject(ABC):

    def __init__(self, cell: Cell):
        self.id: str = str(uuid.uuid4())
        self.cell = cell

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def on_update(self) -> list[GameAction]:
        pass

    @abstractmethod
    def on_draw(self, animation: Animation):
        pass


class GameAction(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def execute(self, room: "Room") -> list[GameAction]:
        pass


class Color(Enum):
    # RED = 31
    # GREEN = 32
    # YELLOW = 33
    # BLUE = 34
    # PURPLE = 35
    # CYAN = 36
    # WHITE = 37
    RED = curses.COLOR_RED
    GREEN = curses.COLOR_GREEN
    YELLOW = curses.COLOR_YELLOW
    BLUE = curses.COLOR_BLUE
    PURPLE = curses.COLOR_MAGENTA
    CYAN = curses.COLOR_CYAN
    WHITE = curses.COLOR_WHITE


class Animation:

    class Symbol:
        def __init__(self, char: str, color: Color = Color.WHITE, z_buffer: int = 0):
            self.char = char
            self.color = color
            self.z_buffer = z_buffer

        def __str__(self):
            return f"\033[{self.color.value}m{self.char}\033[0m"

    def __init__(
        self,
        stdscr: curses.window,
        margin_x: int = 5,
        margin_y: int = 2,
        width: int = 150,
        height: int = 100,
    ):
        self.rect = Rect(
            Cell(margin_x, margin_y), Cell(width + margin_x, height + margin_y)
        )
        self.animation = [
            [Animation.Symbol(" ") for _ in range(0, self.rect.right + 1)]
            for _ in range(0, self.rect.bottom + 1)
        ]
        from roguelike.game_manager import GameManager

        self.gm = GameManager(width=width, height=height, num_of_levels=10)
        self.text = ""
        self.stdscr = stdscr

        for color in Color:
            curses.init_pair(color.value, color.value, curses.COLOR_BLACK)

    def draw(
        self, cell: Cell, symbol: str, color: Color = Color.WHITE, z_buffer: int = 0
    ):
        y = self.rect.top + cell.y
        x = self.rect.left + cell.x
        if self.animation[y][x].z_buffer <= z_buffer:
            self.animation[y][x] = Animation.Symbol(symbol, color)

    def print(self, text):
        self.text = text

    def _clear(self):
        self.animation = [
            [Animation.Symbol(" ") for _ in range(0, self.rect.right + 1)]
            for _ in range(0, self.rect.bottom + 1)
        ]

    def _render(self):
        # os.system("clear")

        for i, row in enumerate(self.animation):
            # self.stdscr.addstr(i, 0, "".join(str(symbol) for symbol in row) + "\n")
            for j, symbol in enumerate(row):
                self.stdscr.addstr(
                    i, j, symbol.char, curses.color_pair(symbol.color.value)
                )
            # print("".join(str(symbol) for symbol in row))
        # print(self.text)
        self.stdscr.refresh()  # Обновляем экран
        self.stdscr.getch()  # Ждём нажатия клавиши

    def _job(self):

        self.gm.init()
        while True:
            self.gm.on_update()
            self.gm.on_draw(self)
            self._render()
            self._clear()
            time.sleep(0.05)

    def _start(self):
        self.t = threading.Thread(target=self._job)
        self.t.start()

    def _stop(self):
        self.t.join()
