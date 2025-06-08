from abc import ABC, abstractmethod
from roguelike.types import Cell, GameAction
from roguelike.types import Animation

counter: int = 0


class GameObject(ABC):

    def __init__(self, cell: Cell):
        self.id: int = counter
        counter += 1
        self.cell = cell

    @abstractmethod
    def on_update(self) -> list[GameAction]:
        pass

    @abstractmethod
    def on_draw(self, animation: Animation):
        pass
