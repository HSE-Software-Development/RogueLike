from typing import List, override
from roguelike.game_actions.create_action import CreateAction
from roguelike.game_objects.player_handling.armory.weapon import (
    Weapon,
    WeaponAttackPattern,
)
from roguelike.game_objects.player_handling.prey import Projectile
from roguelike.types import Cell, Color, GameAction


class RangeWeapon(Weapon):
    def __init__(self, cell, projectile_health):
        super().__init__(cell)

        self.attack_pattern = WeaponAttackPattern.RangeType
        self.attack_speed = 0.5
        self.projectile_health = projectile_health
        self.directions: List[Cell] = [Cell(1, 0)]

    @override
    def on_update(self):
        if self.__is_attack_time():
            new_actions: List[GameAction] = []
            for direction in self.directions:
                new_actions.append(
                    CreateAction(
                        Projectile(self.cell, self.projectile_health, direction)
                    )
                )


class WoodBow(RangeWeapon):
    def __init__(self, cell):
        super().__init__(cell)

        self.attack_speed = 0.5
        self.physical_damage = 15.0
        self.percentage_physical_armor_piercing = 0.0
        self.absolute_physical_armor_piercing = 0

    def on_draw(self, animation):
        animation.draw(self.cell, ")", color=Color.RED, z_buffer=5)
