from roguelike.interfaces.animation import IAnimation
from roguelike.types import Cell, Rect
from roguelike.interfaces import *
from enum import Enum
from typing import Optional, override
from pydantic import BaseModel


class ItemType(Enum):
    SWORD = "sword"
    BOW = "bow"
    POTION = "potion"
    KEY = "key"


class InventoryItem:
    def __init__(self, type: ItemType, object: Optional[IGameObject] = None):
        self.type: ItemType = type
        self.obj: Optional[IGameObject] = object


class Inventory(IGameObject):

    def __init__(self, num_of_slots: int = 5):
        self.items: list[Optional[InventoryItem]] = [None] * num_of_slots
        self.target = 0

    def add_item(
        self, item_type: ItemType, object: Optional[IGameObject] = None
    ) -> bool:
        for i in range(len(self.items)):
            if self.items[i] is None:
                self.items[i] = InventoryItem(type=item_type, object=object)
                return True
        return False

    def remove_item(self, item_type: ItemType) -> bool:
        for i in range(len(self.items)):
            item = self.items[i]
            if item is not None and item.type == item_type:
                self.items[i] = None
                return True
        return False

    def set_target(self, index: int):
        self.target = min(max(0, index), len(self.items) - 1)

    def get_target_item(self) -> Optional[InventoryItem]:
        return self.items[self.target]

    @override
    def on_draw(self, animation: IAnimation):
        pass

    @override
    def on_init(self):
        pass

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        return []
