from roguelike.types import Cell, GameAction, GameObject
from typing import List, override


class MoveAction(GameAction):
    def __init__(self, object: GameObject, cell: Cell):
        self.object = object
        self.cell = cell

    @override
    def execute(self, room) -> list[GameAction]:
        if room.validate_cell(self.cell):
            self.object.cell = self.cell
        return []


class MoveWithChildrenAction(GameAction):
    def __init__(self, object: GameObject, cell: Cell):
        self.object = object
        self.cell = cell

    @override
    def execute(self, room) -> list[GameAction]:
        if room.validate_cell(self.cell):
            self.object.cell = self.cell
            for obj in self.object.children:
                obj.cell = self.cell
        return []


class MoveManyAction(GameAction):
    def __init__(self, objects: List[GameObject], cell: Cell):
        self.objects = objects
        self.cell = cell

    @override
    def execute(self, room) -> list[GameAction]:
        if room.validate_cell(self.cell):
            for obj in self.objects:
                obj.cell = self.cell
        return []
