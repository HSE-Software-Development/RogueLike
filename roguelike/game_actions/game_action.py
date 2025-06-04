from __future__ import annotations
from roguelike.types import Coord
from roguelike.game_objects import GameObject


class GameAction:
    def __init__(self, sender: GameObject, receivers: list[GameObject], coords: list[Coord]):
        self.sender = sender
        self.receivers = receivers
        self.coords = coords
    
    def execute(self) -> list[GameAction]:
        pass