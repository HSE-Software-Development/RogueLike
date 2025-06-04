from typing import List, override
from roguelike.game_objects.player_handling.weapons.weapon import (
    Weapon,
    WeaponAttackPattern,
)
from roguelike.types import Coord


class MeleeWeapon(Weapon):
    def __init__(self, position):
        super().__init__(position)

        self.attack_pattern = WeaponAttackPattern.MeleeType
        self.range = 0

    @override
    def on_update(self):
        attackedCells: List[Coord] = []
        for horizontal_offset in range(1, self.range + 1):
            for vertical_offset in range(1, self.range + 1):
                attackedCells.append(
                    Coord(
                        self.position[0] + horizontal_offset,
                        self.position[1] + vertical_offset,
                    )
                )
        pass


class WoodSword(MeleeWeapon):
    def __init__(self, position):
        super().__init__(position)

        self.range = 1
        self.physical_damage = 10.0
        self.percentage_physical_armor_piercing = 0.0
        self.absolute_physical_armor_piercing = 0
