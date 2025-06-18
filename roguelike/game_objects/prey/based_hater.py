from roguelike.game_actions.haunt_player import HauntPlayerAction
from roguelike.game_actions.move import MoveAction
from .prey import Prey
from roguelike.interfaces import *
from typing import override
from roguelike.types import Cell, Color


class BasedHater(Prey):
    def __init__(self, cell: Cell, health: int, difficulty: float):
        from roguelike.game_objects.armor import Armor
        from roguelike.game_objects.weapons import ProjectileWeapon

        super().__init__(cell, health, Armor(cell), ProjectileWeapon(cell, self))

        self.update_time = 1.0 + int(difficulty)  # per 1 second
        self.weapon.attack_speed = self.update_time
        self.weapon.set_all_damage_params(3 + difficulty * 2, 0, 0, 0, 0, 0)

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        new_actions: list[IGameAction] = []

        new_actions.extend(super().on_update(keyboard))
        if self.is_update_time():
            new_actions.append(HauntPlayerAction(object=self))

        return new_actions

    def on_draw(self, animation):
        animation.draw(self.cell, "z", color=Color.CYAN, z_buffer=5)
