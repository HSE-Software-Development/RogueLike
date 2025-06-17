from roguelike.game_actions.create_action import CreateAction
from roguelike.game_actions.remove_action import RemoveAction
from roguelike.interfaces.animation import IAnimation
from roguelike.types import Cell, Rect
from roguelike.interfaces import *
from enum import Enum
from typing import List, Optional, override
from pydantic import BaseModel


class ItemType(Enum):
    NONE = "none"
    ARMOR = "armor"
    WEAPON = "weapon"
    SWORD = "sword"
    BOW = "bow"
    POTION = "potion"
    KEY = "key"


class InventoryItem:
    def __init__(
        self, object: IGameObjectWithPosition, type: Optional[ItemType] = None
    ):
        if type == None:
            self.type: ItemType = ItemType.NONE
        else:
            self.type: ItemType = type
        self.obj: IGameObjectWithPosition = object


class Inventory(IGameObject):
    def __init__(self, size: int = 5):
        self.current = 0
        self.items: list[Optional[InventoryItem]] = [None] * size

    def drop_item(self) -> List[IGameAction]:
        dropped = self.items[self.current]
        self.items[self.current] = None
        if dropped != None:
            return [CreateAction(dropped.obj)]
        return []

    def add_item(
        self, object: IGameObjectWithPosition, item_type: Optional[ItemType] = None
    ) -> List[IGameAction]:
        new_actions: List[IGameAction] = []

        if object.pickable:
            new_actions.extend(self.drop_item())
            self.items[self.current] = InventoryItem(type=item_type, object=object)
            new_actions.append(RemoveAction(object))

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
