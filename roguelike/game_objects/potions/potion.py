from roguelike.interfaces.animation import IAnimation
from roguelike.interfaces.game_action import IGameAction
from roguelike.interfaces.game_object_with_position import IGameObjectWithPosition
from roguelike.interfaces.keyboard import IKeyboard
from roguelike.types import Cell, Color


class IPotion(IGameObjectWithPosition):
    def __init__(self, cell: Cell, healling_power: float) -> None:
        self.cell = cell
        self.pickable = True
        self.used = False
        self.healling_power = healling_power

    def use(self, prey):
        from roguelike.game_objects.prey.prey import Prey

        if isinstance(prey, Prey):
            prey.health += self.healling_power
        self.used = True

    def on_init(self):
        pass

    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        return []

    def on_draw(self, animation: IAnimation):
        if self.used:
            animation.draw(self.cell, "6", color=Color.GREEN, z_buffer=5)
        else:
            animation.draw(self.cell, "6", color=Color.BLACK_GREEN, z_buffer=5)
