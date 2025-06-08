from roguelike.types import Cell, GameAction
from typing import override


class CreateAction(GameAction):
    def __init__(self, object: GameAction):
        self.object = object

    @override
    def execute(self, room: "Room") -> list[GameAction]:
        room.add_object(self.object)
