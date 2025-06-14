from abc import ABC, abstractmethod
from .game_object_with_position import IGameObjectWithPosition
from roguelike.types import Cell


class IRoom(ABC):
    objects: list[IGameObjectWithPosition]

    @abstractmethod
    def add_object(self, object: IGameObjectWithPosition):
        pass

    @abstractmethod
    def remove_object(self, object: IGameObjectWithPosition):
        pass

    @abstractmethod
    def validate_cell(self, cell: Cell) -> bool:
        pass
