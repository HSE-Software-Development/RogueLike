from roguelike.types import Cell
from roguelike.game_objects import GameObject, Room
from typing import Callable
from roguelike.game_actions import GameAction


class AffectAction(GameAction):
    def __init__(
        self,
        sender: GameObject,
        cell: Cell,
        selfcast: bool,
        affect: Callable[[GameObject], list[GameAction]],
    ):
        self.sender = sender
        self.selfcast = selfcast
        self.affect = affect
        super().__init__(cell=cell)
