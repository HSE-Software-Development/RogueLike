from roguelike.types import Cell, GameObject, GameAction
from typing import Callable, override


class AffectAction(GameAction):
    def __init__(
        self,
        sender: GameObject,
        cells: list[Cell],
        selfcast: bool,
        affect: Callable[[list[GameObject]], list[GameAction]],
    ):
        self.sender = sender
        self.selfcast = selfcast
        self.affect = affect
        self.cells = cells

    @override
    def execute(self, room: "Room") -> list[GameAction]:
        grid: dict[Cell, list[GameObject]] = {}
        for obj in room.objects:
            if obj.cell not in grid:
                grid[obj.cell] = []
            grid[obj.cell].append(obj)

        receivers = []
        for cell in self.cells:
            objects_in_cell = grid[cell]
            for obj in objects_in_cell:
                if obj.id == self.sender and not self.selfcast:
                    continue
                receivers.append(obj)

        return self.affect(receivers)
