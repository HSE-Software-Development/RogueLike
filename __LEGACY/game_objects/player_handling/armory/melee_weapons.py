from typing import List, override
from roguelike.game_actions.damage import DamageAction
from roguelike.game_actions.move import MoveAction
from roguelike.game_objects.player_handling.armory.weapon import (
    Weapon,
    WeaponAttackPattern,
)
from roguelike.types import Cell, Color, GameAction


class MeleeWeapon(Weapon):
    def __init__(self, cell):
        super().__init__(cell)

        self.attack_pattern = WeaponAttackPattern.MeleeType
        self.attack_speed = 0.0
        self.range = 0
        self.attacked_cells: List[Cell] = []

    @override
    def on_update(self) -> List[GameAction]:
        new_actions: List[GameAction] = []
        if self.__is_attack_time():
            for horizontal_offset in range(0, self.range + 1):
                for vertical_offset in range(0, self.range + 1):
                    self.attacked_cells.append(
                        self.cell + Cell(horizontal_offset, vertical_offset)
                    )
            new_actions.append(DamageAction(self, self.attacked_cells, self.hit))
        return new_actions


class WoodSword(MeleeWeapon):
    def __init__(self, cell):
        super().__init__(cell)

        self.attack_speed = 1.0
        self.range = 1
        self.physical_damage = 10.0
        self.percentage_physical_armor_piercing = 0.0
        self.absolute_physical_armor_piercing = 0

    def init(self):
        pass

    def on_draw(self, animation):
        animation.draw(self.cell, "!", color=Color.BLUE, z_buffer=5)

    def on_update(self):
        return []


class ProjectileWeapon(MeleeWeapon):
    def __init__(self, cell, direction):
        super().__init__(cell)

        self.direction = direction

    @override
    def on_update(self) -> List[GameAction]:
        new_actions: List[GameAction] = [MoveAction(self, self.cell + self.direction)]
        new_actions.extend(super().on_update())
        return new_actions
