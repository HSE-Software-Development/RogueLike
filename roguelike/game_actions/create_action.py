from roguelike.game_objects.room import Room
from roguelike.types import Cell, GameAction, GameObject
from typing import override


class CreateAction(GameAction):
    def __init__(self, object: GameObject):
        self.object = object

    @override
    def execute(self, room: Room) -> list[GameAction]:
        room.add_object(self.object)


class DeleteAction(GameAction):
    def __init__(self, object: GameObject):
        self.object = object

    @override
    def execute(self, room: Room) -> list[GameAction]:
        self.object.is_deleted = True
