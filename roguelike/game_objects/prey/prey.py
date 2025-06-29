import time
from roguelike.game_objects.prey.inventory import Inventory, ItemType
from roguelike.game_objects.weapons.melee_weapons.melee_weapon import MeleeWeapon
from roguelike.game_objects.weapons.range_weapons.range_weapon import RangeWeapon
from roguelike.game_objects.weapons.weapon import IWeapon
from roguelike.types import Cell
from roguelike.interfaces import *
from roguelike.game_actions.remove import RemoveAction
from roguelike.game_objects.armor import IArmor
from typing import List, override


class Prey(IGameObjectWithPosition):
    def __init__(self, cell: Cell, health: float, armor: IArmor, weapon: IWeapon):
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
        self.weapon.in_hands = True

        self.children = []
        self.inventory = Inventory(size=5)

        self.inventory.select_item(0)
        armor_type = ItemType.ACTIVE_ARMOR
        self.inventory.add_item(self.armor, armor_type)
        self.children.append(self.armor)

        self.inventory.select_item(1)
        weapon_type = ItemType.ACTIVE_WEAPON
        if isinstance(self.weapon, MeleeWeapon):
            weapon_type = ItemType.ACTIVE_SWORD
        if isinstance(self.weapon, RangeWeapon):
            weapon_type = ItemType.ACTIVE_BOW
        self.inventory.add_item(self.weapon, weapon_type)
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
    def on_init(self):
        pass

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        if self.health <= 0:
            new_actions: List[IGameAction] = []
            new_actions.extend(self.inventory.drop_all())
            new_actions.append(RemoveAction(self))
            return new_actions

        new_actions: List[IGameAction] = []
        for object in self.children:
            new_actions.extend(object.on_update(keyboard))
        return new_actions

    @override
    def on_draw(self, animation: IAnimation):
        pass
