from roguelike.interfaces import *
from typing import override
from roguelike.types import Cell, Color, Effect


class Key(IGameObjectWithPosition):
    def __init__(self, cell: Cell):
        self.cell = cell
        self.children = []

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        return []

    @override
    def on_draw(self, animation: IAnimation):
        animation.draw(
            self.cell + Cell(0, -1),
            "F",
            color=Color.YELLOW,
            effects=[Effect.BOLD, Effect.BLINK],
            z_buffer=5,
        )
        animation.draw(
            self.cell,
            "b",
            color=Color.YELLOW,
            effects=[Effect.BOLD, Effect.BLINK],
            z_buffer=5,
        )

    @override
    def on_init(self):
        pass
