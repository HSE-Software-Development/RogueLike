from roguelike.types import Cell
from roguelike.game_actions import GameAction
from roguelike.game_objects import GameObject


class MoveAction(GameAction):
    def __init__(self, object: GameObject, cell: Cell):
        self.object = object
        super().__init__(cell=cell)
