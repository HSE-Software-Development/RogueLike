from roguelike.game_actions.create import CreateAction
from roguelike.game_actions.remove import RemoveAction
from roguelike.game_objects.armor.armor import Armor
from roguelike.game_objects.weapons.melee_weapons.melee_weapon import MeleeWeapon
from roguelike.game_objects.weapons.range_weapons.range_weapon import RangeWeapon
from roguelike.game_objects.weapons.weapon import Weapon
from roguelike.interfaces.animation import IAnimation
from roguelike.interfaces.item_types import ItemType
from roguelike.types import Cell, Rect
from roguelike.interfaces import *
from enum import Enum
from typing import List, Optional, override
from pydantic import BaseModel


class InventoryItem:
    def __init__(self, item: IGameObjectWithPosition, type: Optional[ItemType] = None):
        if type == None:
            self.type: ItemType = ItemType.NONE
        else:
            self.type: ItemType = type
        self.obj: IGameObjectWithPosition = item


class Inventory(IGameObject):
    def __init__(self, size: int = 5):
        self.current = 0
        self.items: list[Optional[InventoryItem]] = [None] * size

    def drop_item(self) -> List[IRoomGameAction]:
        dropped = self.items[self.current]
        self.items[self.current] = None
        if dropped != None:
            if isinstance(dropped.obj, Weapon):
                dropped.obj.in_hands = False
            return [CreateAction(dropped.obj)]
        return []

    def drop_all(self) -> List[IRoomGameAction]:
        new_actions: List[IRoomGameAction] = []

        for self.current in range(len(self.items)):
            new_actions.extend(self.drop_item())
        self.current = 0

        return new_actions

    def add_item(
        self, item: IGameObjectWithPosition, item_type: Optional[ItemType] = None
    ) -> List[IRoomGameAction]:
        new_actions: List[IRoomGameAction] = []

        if item_type == None or item_type == ItemType.NONE:
            if isinstance(item, Weapon):
                item_type = ItemType.WEAPON
            if isinstance(item, MeleeWeapon):
                item_type = ItemType.SWORD
            if isinstance(item, RangeWeapon):
                item_type = ItemType.BOW
            if isinstance(item, Armor):
                item_type = ItemType.ARMOR

        if item.pickable:
            new_actions.extend(self.drop_item())
            self.items[self.current] = InventoryItem(type=item_type, item=item)
            new_actions.append(RemoveAction(item))

        return new_actions

    def select_item(self, index: int):
        self.current = min(max(0, index), len(self.items) - 1)

    def get_item(self) -> Optional[InventoryItem]:
        return self.items[self.current]

    def remove_key(self):
        for item in self.items:
            if item != None and item.type == ItemType.KEY:
                item = None

    @override
    def on_init(self):
        pass

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        return []

    @override
    def on_draw(self, animation: IAnimation):
        pass
