from roguelike.game_actions.haunt_player import HauntPlayerAction
from roguelike.game_actions.move_action import MoveAction
from .prey import Prey
from roguelike.interfaces import *
from typing import override
from roguelike.types import Cell, Color


class BasedHater(Prey):
    def __init__(self, cell, health):
        from roguelike.game_objects.armor import Armor

        super().__init__(cell=cell, health=health, armor=Armor(cell))

        self.update_time = 0.5

        from roguelike.game_objects.weapons import ProjectileWeapon

        self.projectile_weapon = ProjectileWeapon(self.cell, self)
        self.projectile_weapon.set_all_damage_params(3, 0, 0, 0, 0, 0)

        self.children.append(self.projectile_weapon)

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        new_actions: list[IGameAction] = []

        new_actions.extend(super().on_update(keyboard=keyboard))
        new_actions.extend(self.projectile_weapon.on_update(keyboard=keyboard))
        if self.is_update_time():
            new_actions.append(HauntPlayerAction(object=self))

        return new_actions

    def on_draw(self, animation):
        animation.draw(self.cell, "z", color=Color.CYAN, z_buffer=5)
