from roguelike.types import Cell, Color
from .range_weapon import RangeWeapon
from typing import override


class WoodBow(RangeWeapon):
    def __init__(self, cell):
        super().__init__(cell, projectile_health=2)

        self.attack_speed = 0.5
        self.physical_damage = 6.0
        self.percentage_physical_armor_piercing = 0.0
        self.absolute_physical_armor_piercing = 0
        self.projectile_velocity = 10.0

    @override
    def on_draw(self, animation):
        animation.draw(self.cell, ")", color=Color.BLACK_PURPLE, z_buffer=4)


class StrongBow(RangeWeapon):
    def __init__(self, cell):
        super().__init__(cell, projectile_health=15)

        self.attack_speed = 5
        self.physical_damage = 25.0
        self.percentage_physical_armor_piercing = 10.0
        self.absolute_physical_armor_piercing = 0
        self.projectile_velocity = 100.0

    @override
    def on_draw(self, animation):
        animation.draw(self.cell, ")", color=Color.BLACK_YELLOW, z_buffer=4)
