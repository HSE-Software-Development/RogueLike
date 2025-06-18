from .melee_weapon import MeleeWeapon
from roguelike.types import Color
from typing import override


class WoodSword(MeleeWeapon):
    def __init__(self, cell):
        super().__init__(cell)

        self.attack_speed = 1.0
        self.range = 1
        self.physical_damage = 10.0
        self.percentage_physical_armor_piercing = 0.0
        self.absolute_physical_armor_piercing = 0

    @override
    def on_draw(self, animation):
        animation.draw(self.cell, "!", color=Color.BLUE, z_buffer=4)
