from roguelike.interfaces import *
from .melee_weapon import MeleeWeapon
from typing import override


class ProjectileWeapon(MeleeWeapon):
    def __init__(self, cell, owner):
        super().__init__(cell)

        self.owner = owner
