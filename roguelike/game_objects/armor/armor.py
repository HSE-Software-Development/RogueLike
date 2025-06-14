from roguelike.interfaces import *
from roguelike.types import Cell
from typing import override


class Armor(IGameObjectWithPosition):
    def __init__(self, cell):
        self.cell = cell
        self.children = []
        self.physical_armor = 0.0
        self.magical_armor = 0.0

        # who knows, knows
        self.vanguard_effect = 0.0

    @override
    def on_init(self):
        pass

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        return []

    @override
    def on_draw(self, animation: IAnimation):
        pass
