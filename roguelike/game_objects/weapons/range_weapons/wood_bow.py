from roguelike.types import Cell, Color
from .range_weapon import RangeWeapon
from typing import override


class WoodBow(RangeWeapon):
    def __init__(self, cell):
        super().__init__(cell, projectile_health=10)

        self.attack_speed = 0.5
        self.physical_damage = 15.0
        self.percentage_physical_armor_piercing = 0.0
        self.absolute_physical_armor_piercing = 0

    @override
    def on_draw(self, animation):
        animation.draw(self.cell, ")", color=Color.BLUE, z_buffer=5)
