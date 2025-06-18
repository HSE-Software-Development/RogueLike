from typing import List, override
from roguelike.game_actions.create import CreateAction
from ..weapon import Weapon, WeaponAttackPattern
from roguelike.types import Cell, Color
from roguelike.interfaces import *


class RangeWeapon(Weapon):
    def __init__(self, cell, projectile_health):
        super().__init__(cell)

        self.attack_pattern = WeaponAttackPattern.RangeType
        self.attack_speed = 0.5
        self.projectile_health = projectile_health
        self.directions: List[Cell] = [Cell(1, 0)]

    @override
    def on_update(self, keyboard: IKeyboard) -> List[IGameAction]:
        from roguelike.game_objects.prey import Projectile

        if self.in_hands and self.is_attack_time():
            new_actions: List[IGameAction] = []
            for direction in self.directions:
                projectileObj = Projectile(
                    cell=self.cell + direction,
                    health=self.projectile_health,
                    direction=direction,
                )
                projectileObj.weapon.set_same(self)
                new_actions.append(CreateAction(projectileObj))
            return new_actions
        return []
