from roguelike.interfaces import *
from .melee_weapon import MeleeWeapon
from typing import override


class ProjectileWeapon(MeleeWeapon):
    def __init__(self, cell, direction):
        super().__init__(cell)
        self.direction = direction

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        from roguelike.game_actions import MoveAction

        return [MoveAction(cell=self.cell + self.direction, object=self)]
