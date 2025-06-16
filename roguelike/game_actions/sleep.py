from time import sleep
from roguelike.interfaces import *
from roguelike.types import Cell
from typing import override


class SleepAction(IRoomGameAction):
    def __init__(self, duration):
        self.duration = duration  # floating number of seconds

    @override
    def room_handler(self, room: IRoom):
        sleep(self.duration)
