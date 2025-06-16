from ..weapon import Weapon, WeaponAttackPattern
from roguelike.types import Cell
from roguelike.interfaces import *
from typing import override


class MeleeWeapon(Weapon):
    def __init__(self, cell):
        super().__init__(cell)

        self.attack_pattern = WeaponAttackPattern.MeleeType
        self.attack_speed = 0.0
        self.range = 0
        self.attacked_cells: list[Cell] = []

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        from roguelike.game_actions.damage_action import DamageAction

        new_actions: list[IGameAction] = []
        if self._is_attack_time():
            for horizontal_offset in range(0, self.range + 1):
                for vertical_offset in range(0, self.range + 1):
                    self.attacked_cells.clear()
                    self.attacked_cells.append(
                        self.cell + Cell(horizontal_offset, vertical_offset)
                    )
            new_actions.append(
                DamageAction(sender=self, cells=self.attacked_cells, hit=self.hit)
            )
        return new_actions
