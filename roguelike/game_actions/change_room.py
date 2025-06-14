from roguelike.interfaces import *
from typing import override


class ChangeRoomAction(ILevelGameAction):

    def __init__(self, prev_room: int, next_room: int, door_index: int):
        self.prev_room = prev_room
        self.next_room = next_room
        self.door_index = door_index

    @override
    def level_handler(self, level: ILevel):
        level.move_player(self.prev_room, self.next_room, self.door_index)
