from roguelike.interfaces import *
from roguelike.types import Cell
from typing import override


class HauntPlayerAction(IRoomGameAction):
    def __init__(self, object: IGameObjectWithPosition):
        self.object = object

    @override
    def room_handler(self, room: IRoom):
        from roguelike.game_objects.prey.projectile import Projectile
        from roguelike.game_objects.room import Room

        if isinstance(room, Room) and room.player is not None:
            cell = self.object.cell + (room.player.cell - self.object.cell).normalize()
            if room.validate_cell(cell):
                self.object.cell = cell
                for child in self.object.children:
                    child.cell = cell
            elif isinstance(self.object, Projectile):
                self.object.health = 0
