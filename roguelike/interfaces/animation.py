from __future__ import annotations
from abc import ABC, abstractmethod
from roguelike.types import Cell, Color, Effect, Rect


def with_area(
    animation: IAnimation, width: int, height: int, margin_x: int = 0, margin_y: int = 0
) -> IAnimation:
    class Wrapper(IAnimation):
        def __init__(
            self,
            animation: IAnimation,
            width: int,
            height: int,
            margin_x: int = 0,
            margin_y: int = 0,
        ):
            self.animation = animation
            self.margin_x = margin_x
            self.margin_y = margin_y
            self.width = width
            self.height = height

        def draw(
            self,
            cell: Cell,
            char: str,
            color: Color = Color.WHITE,
            effects: list[Effect] = [],
            z_buffer: int = 0,
        ):
            if (
                cell.x < 0
                or cell.y < 0
                or cell.x >= self.width
                or cell.y >= self.height
            ):
                return

            cell = Cell(cell.x + self.margin_x, cell.y + self.margin_y)
            self.animation.draw(cell, char, color, effects, z_buffer)

        def print(self, text):
            self.animation.print(text)

    return Wrapper(animation, width, height, margin_x, margin_y)


class IAnimation(ABC):
    @abstractmethod
    def draw(
        self,
        cell: Cell,
        char: str,
        color: Color = Color.WHITE,
        effects: list[Effect] = [],
        z_buffer: int = 0,
    ):
        pass

    @abstractmethod
    def print(self, text):
        pass

    def with_area(
        self, width: int, height: int, margin_x: int = 0, margin_y: int = 0
    ) -> IAnimation:
        return with_area(self, width, height, margin_x, margin_y)
