from roguelike.types import Cell
from roguelike.interfaces import *
from typing import Callable, override


class DamageAction(IRoomGameAction):
    def __init__(
        self,
        hit: Callable[[list[IGameObject]]],
        cells: list[Cell],
    ):
        self.hit = hit
        self.cells = cells

    @override
    def room_handler(self, room: IRoom):
        from roguelike.game_objects.player_handling.prey import Prey

        grid: dict[Cell, list[GameObject]] = {}
        for obj in room.objects:
            if not obj.is_deleted:
                if obj.cell not in grid:
                    grid[obj.cell] = []
                grid[obj.cell].append(obj)

        receivers = []
        for cell in self.cells:
            objects_in_cell = grid[cell]
            for obj in objects_in_cell:
                if obj.is_deleted or obj.id == self.sender or not isinstance(obj, Prey):
                    continue
                receivers.append(obj)

        return self.weapon.hit(receivers)
