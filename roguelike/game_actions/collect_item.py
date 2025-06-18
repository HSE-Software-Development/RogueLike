from roguelike.interfaces.item_types import ItemType
from roguelike.types import Cell
from roguelike.interfaces import *
from typing import Callable, List, override


class CollectItemAction(IRoomGameAction):
    def __init__(
        self,
        cells: List[Cell],
        collect: Callable[[IGameObjectWithPosition, ItemType], List[IRoomGameAction]],
    ):
        self.cells = cells
        self.collect = collect

    @override
    def room_handler(self, room: IRoom):
        new_actions: List[IRoomGameAction] = []
        for cell in self.cells:
            for obj in room.objects:
                if not obj.pickable:
                    continue
                if obj.cell == cell:
                    new_actions = self.collect(obj, ItemType.NONE)
        for action in new_actions:
            action.room_handler(room)
