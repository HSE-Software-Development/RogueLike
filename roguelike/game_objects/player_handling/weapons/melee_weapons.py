from typing import List, override
from roguelike.game_objects.player_handling.weapons.weapon import (
    Weapon,
    WeaponAttackPattern,
)
from roguelike.types import Cell


class MeleeWeapon(Weapon):
    def __init__(self, cell):
        super().__init__(cell)

        self.attack_pattern = WeaponAttackPattern.MeleeType
        self.range = 0

    @override
    def on_update(self):
        attackedCells: List[Cell] = []
        for horizontal_offset in range(1, self.range + 1):
            for vertical_offset in range(1, self.range + 1):
                attackedCells.append(
                    self.cell + Cell(horizontal_offset, vertical_offset)
                )
        pass


class WoodSword(MeleeWeapon):
    def __init__(self, cell):
        super().__init__(cell)

        self.range = 1
        self.physical_damage = 10.0
        self.percentage_physical_armor_piercing = 0.0
        self.absolute_physical_armor_piercing = 0
