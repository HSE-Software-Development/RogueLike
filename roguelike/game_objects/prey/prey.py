import time
from roguelike.types import Cell
from roguelike.interfaces import *
from roguelike.game_actions.remove_action import RemoveAction
from roguelike.game_objects.armor import Armor
from typing import override


class Prey(IGameObjectWithPosition):
    def __init__(self, cell: Cell, health: float, armor: Armor):
        self.cell = cell
        self.children = []
        self.max_health = health
        self.health = health
        self.armor = (
            armor  # совсем не важно, как ты ударишь, а важно, какой держишь удар
        )

        self.update_time = 2.0  # per 1 second
        self.previous_time = -1.0

    def is_update_time(self) -> bool:
        current_time = time.monotonic()

        if self.previous_time == -1.0:
            self.previous_time = current_time
        elapsed_time = current_time - self.previous_time

        if self.update_time == 0.0 or elapsed_time >= 1.0 / self.update_time:
            self.previous_time = current_time
            return True
        return False

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        if self.health <= 0:
            return [RemoveAction(self)]
        return []

    @override
    def on_draw(self, animation: IAnimation):
        pass

    @override
    def on_init(self):
        pass
