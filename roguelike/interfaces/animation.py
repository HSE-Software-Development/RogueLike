from abc import ABC, abstractmethod
from roguelike.types import Cell, Color


class IAnimation(ABC):
    @abstractmethod
    def draw(
        self, cell: Cell, char: str, color: Color = Color.WHITE, z_buffer: int = 0
    ):
        pass

    @abstractmethod
    def print(self, text):
        pass
