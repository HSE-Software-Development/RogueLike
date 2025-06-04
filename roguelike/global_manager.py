from __future__ import annotations
from abc import ABC, abstractmethod
from typing import override
from roguelike.game_objects import Level, GameObject
from roguelike.actions import GameAction
from roguelike.types import Coord


class GlobalManager:
    
    def __init__(self):
        self.level = Level()
        self.frame: dict[Coord, list[GameObject]]
        pass

    def run(self):
        actions: list[GameAction] = self.level.on_update()
        while True:
            for action in actions:
                for coord in action.coords:
                    objects = self.frame[coord]
                    for obj in objects:
                        if obj.id == action.sender: # todo ???
                            continue
                        action.receivers.append(obj)
                
            new_actions: list[GameAction] = []
            for action in actions:
                new_actions.extend(action.execute())

            actions = new_actions



            