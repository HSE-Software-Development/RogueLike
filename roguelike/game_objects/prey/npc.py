from .prey import Prey
from roguelike.interfaces import *
from roguelike.types import Cell
from roguelike.game_objects.armor import Armor
from roguelike.game_objects.weapons import Weapon
from typing import override


class NPC(Prey):
    def __init__(self, cell: Cell, health: int, armor: Armor, weapon: Weapon):
        super().__init__(cell=cell, health=health, armor=armor)

        self.armor = armor
        self.weapon = weapon

        self.children.append(self.armor)
        self.children.append(self.weapon)

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        new_actions: list[IGameAction] = []
        for object in self.children:
            new_actions.extend(object.on_update(keyboard))
        new_actions.extend(super().on_update(keyboard))
        return new_actions
