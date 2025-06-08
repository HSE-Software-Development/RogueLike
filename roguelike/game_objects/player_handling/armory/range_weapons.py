from typing import List, override
from roguelike.game_objects.player_handling.armory.weapon import (
    Weapon,
    WeaponAttackPattern,
)
from roguelike.types import Cell


class RangeWeapon(Weapon):
    def __init__(self, cell):
        super().__init__(cell)

        self.attack_pattern = WeaponAttackPattern.RangeType
        self.attack_speed = 0.5
        self.direction = Cell(1, 0)

    @override
    def on_update(self):
        if self.__is_attack_time():
            damage = self.__calculate_damage()
            projectileCellSpawn = self.cell + self.direction


class WoodBow(RangeWeapon):
    def __init__(self, cell):
        super().__init__(cell)

        self.attack_speed = 0.5
        self.physical_damage = 15.0
        self.percentage_physical_armor_piercing = 0.0
        self.absolute_physical_armor_piercing = 0
