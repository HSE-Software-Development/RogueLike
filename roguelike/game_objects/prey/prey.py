import time
from roguelike.game_objects.prey.inventory import Inventory, ItemType
from roguelike.game_objects.weapons.weapon import Weapon
from roguelike.types import Cell
from roguelike.interfaces import *
from roguelike.game_actions.remove_action import RemoveAction
from roguelike.game_objects.armor import Armor
from typing import List, override


class Prey(IGameObjectWithPosition):
    def __init__(self, cell: Cell, health: float, armor: Armor, weapon: Weapon):
        self.cell = cell
        self.pickable = False

        self.update_time = 25.0  # per 1 second
        self.previous_time = -1.0

        self.max_health = health
        self.health = health

        self.armor = (
            armor  # совсем не важно, как ты ударишь, а важно, какой держишь удар
        )
        self.weapon = weapon  # Или нет?..

        self.children = []
        self.inventory = Inventory(size=5)

        self.inventory.select_item(0)
        self.inventory.add_item(self.armor, ItemType.ARMOR)
        self.children.append(self.armor)

        self.inventory.select_item(1)
        self.inventory.add_item(self.weapon, ItemType.WEAPON)
        self.children.append(self.weapon)

    def is_update_time(self) -> bool:
        current_time = time.monotonic()

        if self.previous_time == -1.0:
            self.previous_time = current_time
        elapsed_time = current_time - self.previous_time

        if self.update_time == 0.0 or elapsed_time >= 1.0 / self.update_time:
            self.previous_time = current_time
            return True
        return False

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        if self.health <= 0:
            return [RemoveAction(self)]

        new_actions: List[IGameAction] = []
        for object in self.children:
            new_actions.extend(object.on_update(keyboard))
        return new_actions

    @override
    def on_draw(self, animation: IAnimation):
        pass

    @override
    def on_init(self):
        pass
