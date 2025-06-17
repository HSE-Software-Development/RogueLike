from roguelike.game_actions.create_action import CreateAction
from roguelike.game_actions.game_over import GameOverAction
from roguelike.game_actions.remove_action import RemoveAction
from roguelike.game_actions.sleep import SleepAction
from roguelike.game_objects.game_over import GameOver
from .npc import NPC
from roguelike.game_objects.armor import Armor
from roguelike.types import Cell, Color, Effect
from roguelike.interfaces import *
from roguelike.game_objects.weapons import Weapon
from roguelike.game_objects.weapons.range_weapons.range_weapon import RangeWeapon
from roguelike.game_actions import MoveAction
from typing import override
from .inventory import Inventory


class Player(NPC):
    def __init__(
        self,
        cell: Cell,
        health: int,
        armor: Armor,
        weapon: Weapon,
        inventory: Inventory,
    ):
        super().__init__(cell, health, armor=armor, weapon=weapon)

        self.update_time = 10.0  # per 1 second

        self.direction = Cell(1, 0)

        self.armor.cell = self.cell
        self.weapon.cell = self.cell
        self.children.append(self.armor)
        self.children.append(self.weapon)

        self.delayed_attack = False
        self.inventory = inventory

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        if keyboard.is_pressed("o"):
            self.delayed_attack = True

        if not self.is_update_time():
            return []

        new_actions: list[IGameAction] = []

        if keyboard.is_pressed("w"):
            self.direction = Cell(0, -1)
            new_actions.append(MoveAction(object=self, cell=self.cell + self.direction))
        elif keyboard.is_pressed("s"):
            self.direction = Cell(0, 1)
            new_actions.append(MoveAction(object=self, cell=self.cell + self.direction))
        elif keyboard.is_pressed("a"):
            self.direction = Cell(-1, 0)
            new_actions.append(MoveAction(object=self, cell=self.cell + self.direction))
        elif keyboard.is_pressed("d"):
            self.direction = Cell(1, 0)
            new_actions.append(MoveAction(object=self, cell=self.cell + self.direction))

        if isinstance(self.weapon, RangeWeapon):
            if len(self.weapon.directions) == 1:
                self.weapon.directions = [self.direction]

        if self.delayed_attack:
            new_actions.extend(self.weapon.on_update(keyboard))
            self.delayed_attack = False

        if self.health <= 0:
            return [RemoveAction(self), SleepAction(1.5), GameOverAction()]

        return new_actions

    def on_draw(self, animation):
        for child in self.children:
            child.on_draw(animation)
        animation.draw(self.cell, "*", color=Color.BLACK_RED, z_buffer=5)
