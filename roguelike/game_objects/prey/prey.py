from roguelike.types import Cell
from roguelike.interfaces import *
from roguelike.game_actions.remove_action import RemoveAction
from roguelike.game_objects.armor import Armor
from typing import override


class Prey(IGameObjectWithPosition):
    def __init__(self, cell: Cell, health: float, armor: Armor):
        self.cell = cell
        self.children = []
        self.health = health
        self.armor = (
            armor  # совсем не важно, как ты ударишь, а важно, какой держишь удар
        )

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        if self.health <= 0:
            return [RemoveAction(self)]
        return []

    @override
    def on_draw(self, animation: IAnimation):
        pass

    @override
    def on_init(self):
        pass
