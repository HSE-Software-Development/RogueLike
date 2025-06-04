from roguelike.types import Cell
from roguelike.game_objects import GameObject, Room
from typing import Callable
from roguelike.game_actions import GameAction


class AffectAction(GameAction):
    def __init__(
        self, sender: GameObject, cell: Cell, affect: Callable[[GameObject], None]
    ):
        self.sender = sender
        super().__init__(cell=cell)
