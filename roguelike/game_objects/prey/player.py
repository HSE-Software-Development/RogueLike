from .npc import NPC
from roguelike.game_objects.armor import Armor
from roguelike.types import Cell, Color, Effect
from roguelike.interfaces import *
from roguelike.game_objects.weapons import Weapon
from roguelike.game_actions import MoveAction
from typing import override


class Player(NPC):
    def __init__(self, cell: Cell, health: int, armor: Armor, weapon: Weapon):
        super().__init__(cell, health, armor=armor, weapon=weapon)
        self.children.append(self.armor)
        self.children.append(self.weapon)

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        new_actions: list[IGameAction] = []

        if keyboard.is_pressed("w"):
            new_actions.append(
                MoveAction(object=self, cell=Cell(self.cell.x, self.cell.y - 1))
            )
        elif keyboard.is_pressed("s"):
            new_actions.append(
                MoveAction(object=self, cell=Cell(self.cell.x, self.cell.y + 1))
            )
        elif keyboard.is_pressed("a"):
            new_actions.append(
                MoveAction(object=self, cell=Cell(self.cell.x - 1, self.cell.y))
            )
        elif keyboard.is_pressed("d"):
            new_actions.append(
                MoveAction(object=self, cell=Cell(self.cell.x + 1, self.cell.y))
            )

        new_actions.extend(super().on_update(keyboard))

        return new_actions

    def on_draw(self, animation):
        animation.draw(self.cell, "8", color=Color.RED, z_buffer=5)
