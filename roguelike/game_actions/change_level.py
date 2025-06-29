from roguelike.interfaces import *
from typing import override


class ChangeLevelAction(IManagerGameAction):

    def __init__(self, room_index: int):
        self.room_index = room_index

    @override
    def manager_handler(self, manager: IManager):
        manager.next_level(room_index=self.room_index)
