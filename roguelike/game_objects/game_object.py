from abc import ABC, abstractmethod
from roguelike.types import Cell

counter: int = 0


class GameObject(ABC):

    def __init__(self, cell: Cell):
        self.id: int = counter
        counter += 1
        self.cell = cell

    @abstractmethod
    def on_update(self):
        pass

    @abstractmethod
    def on_draw():
        pass
