from roguelike.game_objects.potions.potion import IPotion
from roguelike.types import Cell


class SmallHealingPotion(IPotion):
    def __init__(self, cell: Cell) -> None:
        super().__init__(cell, 3.0)


class BigHealingPotion(IPotion):
    def __init__(self, cell: Cell) -> None:
        super().__init__(cell, 7.0)


class PoisonedHealingPotion(IPotion):
    def __init__(self, cell: Cell) -> None:
        super().__init__(cell, -2.0)
