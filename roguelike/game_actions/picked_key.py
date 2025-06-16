from roguelike.interfaces import *
from roguelike.types import Cell
from typing import override


class PickedKey(ILevelGameAction):
    def __init__(self, room_index: int):
        self.room_index = room_index

    @override
    def level_handler(self, level: ILevel):
        level.picked_key(self.room_index)
