from __future__ import annotations
from abc import ABC, abstractmethod
from typing import override
from roguelike.types import Cell, GameObject, GameAction, Animation
from roguelike.game_objects import Level
from roguelike.types import Rect, Cell


class GameManager(GameObject):
    def __init__(self, width: int = 150, height: int = 100, num_of_levels: int = 10):
        rect = Rect(lt=Cell(0, 0), rb=Cell(width, height))

        self.current_level = 0
        self.levels: list[Level] = []
        self.levels.append(
            Level(rect=rect, level_type=Level.LevelType.START, difficulty=0.0)
        )
        for i in range(1, num_of_levels - 1):
            difficulty = i / (num_of_levels - 2)
            self.levels.append(
                Level(
                    rect=rect, level_type=Level.LevelType.COMMON, difficulty=difficulty
                )
            )
        self.levels.append(
            Level(rect=rect, level_type=Level.LevelType.FINISH, difficulty=1.0)
        )

    @override
    def init(self):
        for level in self.levels:
            level.init()

    @override
    def on_draw(self, animation: Animation):
        self.levels[self.current_level].on_draw(animation)

    @override
    def on_update(self):
        self.levels[self.current_level].on_update()
