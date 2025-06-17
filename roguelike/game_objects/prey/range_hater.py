from roguelike.game_actions.haunt_player import HauntPlayerAction
from roguelike.game_actions.move_action import MoveAction
from .prey import Prey
from roguelike.interfaces import *
from typing import override
from roguelike.types import Cell, Color


class RangeHater(Prey):
    def __init__(self, cell, health, diffculty: float):
        from roguelike.game_objects.armor import Armor
        from roguelike.game_objects.weapons.range_weapons.wood_bow import WoodBow

        super().__init__(cell, health, Armor(cell), WoodBow(cell))

        self.direction = Cell(0, 0)
        self.update_time = 1.0 + diffculty * 3  # per 1 second

        self.weapon.attack_speed = self.update_time
        self.weapon.set_all_damage_params(3, 0, 0, 0, 0, 0)

        self.children.append(self.weapon)

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        new_actions: list[IGameAction] = []

        new_actions.extend(super().on_update(keyboard))
        new_actions.extend(self.weapon.on_update(keyboard))

        return new_actions

    def on_draw(self, animation):
        animation.draw(self.cell, "E", color=Color.PURPLE, z_buffer=5)
