from .armor import Armor
from typing import override
from roguelike.interfaces import *
from roguelike.types import Color


class OldRobe(Armor):
    def __init__(self, position):
        super().__init__(position)

        self.physical_armor = 2.0
        self.magical_armor = 1.0

    @override
    def on_draw(self, animation: IAnimation):
        animation.draw(self.cell, "&", color=Color.BLACK_GREEN, z_buffer=4)


class BronzeArmor(Armor):
    def __init__(self, position):
        super().__init__(position)

        self.physical_armor = 10.0
        self.magical_armor = 5.0

    @override
    def on_draw(self, animation: IAnimation):
        animation.draw(self.cell, "&", color=Color.BLACK_YELLOW, z_buffer=4)
