from typing import List, override
from roguelike.game_objects.player_handling.armory.weapon import (
    Weapon,
    WeaponAttackPattern,
)
from roguelike.types import Cell


class MeleeWeapon(Weapon):
    def __init__(self, cell):
        super().__init__(cell)

        self.attack_pattern = WeaponAttackPattern.MeleeType
        self.attack_speed = 0.0
        self.range = 0
        self.attackedCells: List[Cell] = []

    @override
    def on_update(self):
        if self.__is_attack_time():
            damage = self.__calculate_damage()
            for horizontal_offset in range(0, self.range + 1):
                for vertical_offset in range(0, self.range + 1):
                    self.attackedCells.append(
                        self.cell + Cell(horizontal_offset, vertical_offset)
                    )


class WoodSword(MeleeWeapon):
    def __init__(self, cell):
        super().__init__(cell)

        self.attack_speed = 1.0
        self.range = 1
        self.physical_damage = 10.0
        self.percentage_physical_armor_piercing = 0.0
        self.absolute_physical_armor_piercing = 0


class Projectile(MeleeWeapon):
    def __init__(self, cell, direction):
        super().__init__(cell)

        self.direction = direction

    def on_update(self):
        super().on_update()
        # move on direction
