from roguelike.game_actions.move import MoveAction
from .prey import Prey
from roguelike.interfaces import *
from typing import override
from roguelike.types import Cell, Color


class Projectile(Prey):
    def __init__(self, cell: Cell, health: float, direction: Cell):
        from roguelike.game_objects.armor import IArmor
        from roguelike.game_objects.weapons import ProjectileWeapon

        super().__init__(cell, health, IArmor(cell), ProjectileWeapon(cell, self))

        self.direction = direction
        self.update_time = 5.0
        self.weapon.attack_speed = self.update_time

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        new_actions: list[IGameAction] = []

        new_actions.extend(super().on_update(keyboard))
        if self.is_update_time():
            new_actions.append(MoveAction(object=self, cell=self.cell + self.direction))

        return new_actions

    def on_draw(self, animation):
        animation.draw(self.cell, "~", color=Color.WHITE, z_buffer=7)
