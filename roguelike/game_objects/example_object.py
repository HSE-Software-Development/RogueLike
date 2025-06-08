from roguelike.types import GameObject, GameAction, Cell, Animation, Color
from roguelike.keyboard import is_pressed
from roguelike.game_actions import MoveAction
from typing import override


class ExampleObject(GameObject):

    def __init__(self, position: Cell):
        super().__init__(position)

    @override
    def init(self):
        pass

    @override
    def on_update(self) -> list[GameAction]:
        if is_pressed("w"):
            return [MoveAction(self, Cell(self.cell.x, self.cell.y - 1))]
        elif is_pressed("s"):
            return [MoveAction(self, Cell(self.cell.x, self.cell.y + 1))]
        elif is_pressed("a"):
            return [MoveAction(self, Cell(self.cell.x - 1, self.cell.y))]
        elif is_pressed("d"):
            return [MoveAction(self, Cell(self.cell.x + 1, self.cell.y))]
        return []

    @override
    def on_draw(self, animation: Animation):
        animation.draw(self.cell, "8", color=Color.RED, z_buffer=4)
        # animation.print("ExampleObject at ")
