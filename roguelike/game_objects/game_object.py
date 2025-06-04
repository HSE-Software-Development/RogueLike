from abc import ABC, abstractmethod
from roguelike.types import Coord

counter: int = 0


class GameObject(ABC):

    def __init__(self, position: Coord):
        self.id: int = counter
        counter += 1
        self.position = position

    @abstractmethod
    def on_update(self):
        pass

    @abstractmethod
    def on_draw():
        pass
