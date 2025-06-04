from roguelike.types import Cell
from roguelike.game_actions import GameAction


class CreateAction(GameAction):
    def __init__(self, object_to_create: GameAction, cell: Cell):
        self.object_to_create = object_to_create
        super().__init__(cell=cell)
