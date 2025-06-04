from game_objects import GameObject, Room
from typing import override


class Level(GameObject):

    def __init__(self):
        self.rooms: list[Room] = []

    @override
    def on_draw(self):
        for room in self.rooms:
            room.on_draw()

    @override
    def on_update(self):
        for room in self.rooms:
            room.on_update()
