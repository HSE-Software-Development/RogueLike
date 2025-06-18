from roguelike.game_objects.potions.potion import Potion
from roguelike.types import Cell


class SmallHealingPotion(Potion):
    def __init__(self, cell: Cell) -> None:
        super().__init__(cell, 3.0)


class BigHealingPotion(Potion):
    def __init__(self, cell: Cell) -> None:
        super().__init__(cell, 7.0)


class PoisonedHealingPotion(Potion):
    def __init__(self, cell: Cell) -> None:
        super().__init__(cell, -2.0)
