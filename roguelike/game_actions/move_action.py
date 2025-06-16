from roguelike.interfaces import *
from roguelike.types import Cell
from typing import override


class MoveAction(IRoomGameAction):
    def __init__(self, cell: Cell, object: IGameObjectWithPosition):
        self.cell = cell
        self.object = object

    @override
    def room_handler(self, room: IRoom):
        from roguelike.game_objects.prey.projectile import Projectile

        if room.validate_cell(self.cell):
            self.object.cell = self.cell
            for child in self.object.children:
                child.cell = self.cell
        elif isinstance(self.object, Projectile):
            self.object.health = 0
