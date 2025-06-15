from roguelike.interfaces import *
from typing import override


class ChangeLevelAction(IManagerGameAction, ILevelGameAction):

    def __init__(self, room_index: int):
        self.room_index = room_index

    @override
    def manager_handler(self, manager: IManager):
        manager.next_level()

    @override
    def level_handler(self, level: ILevel):
        level.remove_player(self.room_index)
