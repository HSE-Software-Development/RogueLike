from roguelike.types import Cell, GameAction, GameObject
from typing import override


class MoveAction(GameAction):
    def __init__(self, object: GameObject, cell: Cell):
        self.object = object
        self.cell = cell

    @override
    def execute(self, room) -> list[GameObject]:
        if not room.validate_cell(self.cell):
            return []
        self.object.cell = self.cell
        return []
