from .prey import Prey
from roguelike.interfaces import *
from typing import override
from roguelike.types import Cell, Color


class Projectile(Prey):
    def __init__(self, cell, health, direction):
        from roguelike.game_objects.armor import Armor

        armor = Armor(cell)
        super().__init__(cell=cell, health=health, armor=armor)

        from roguelike.game_objects.weapons import ProjectileWeapon

        self.projectile_weapon = ProjectileWeapon(cell, direction)

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        new_actions: list[IGameAction] = []
        new_actions.extend(super().on_update(keyboard=keyboard))

        new_actions.extend(self.projectile_weapon.on_update(keyboard=keyboard))
        return new_actions

    def on_draw(self, animation):
        animation.draw(self.cell, "~", color=Color.BLUE, z_buffer=5)
