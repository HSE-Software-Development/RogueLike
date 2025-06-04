from __future__ import annotations
from roguelike.types import Cell
from roguelike.game_objects import GameObject, Room
from typing import Callable


class GameAction:
    def __init__(
        self,
        cell: list[Cell],
    ):
        self.cell = cell


class MoveAction(GameAction):
    def __init__(self, object: GameObject, cell: Cell):
        self.object = object
        super().__init__(cell=cell)


class CreateAction(GameAction):
    def __init__(self, object_to_create: GameAction, cell: Cell):
        self.object_to_create = object_to_create
        super().__init__(cell=cell)


class AffectAction(GameAction):
    def __init__(
        self, sender: GameObject, cell: Cell, affect: Callable[[GameObject], None]
    ):
        self.sender = sender
        super().__init__(cell=cell)
