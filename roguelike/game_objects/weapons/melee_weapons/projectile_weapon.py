from roguelike.interfaces import *
from roguelike.interfaces import IAnimation
from roguelike.types import Color
from .melee_weapon import MeleeWeapon
from typing import override


class ProjectileWeapon(MeleeWeapon):
    def __init__(self, cell, owner):
        super().__init__(cell)

        self.owner = owner
        self.pickable = False

    def on_draw(self, animation: IAnimation):
        animation.draw(self.cell, "Z", color=Color.GREEN, z_buffer=5)
