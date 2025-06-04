from game_objects import GameObject
from roguelike.game_actions import GameAction, MoveAction, CreateAction, AffectAction
from roguelike.types import Cell
from typing import override


class Room(GameObject):

    def __init__(self):
        self.objects: list[GameObject] = []
        self.actions: list[GameAction] = []
        self.grid: dict[Cell, list[GameObject]]

    @override
    def on_draw(self):
        pass

    @override
    def on_update(self):
        actions: list[GameAction] = []
        for obj in self.objects:
            actions.extend(obj.on_update())

        for action in actions:
            self.execute_action(action)

        for action in actions:

        new_actions: list[GameAction] = []
        for action in actions:
            self.execute_action(action)

        actions = new_actions

    def execute_action(self, action: GameAction):
        if isinstance(action, MoveAction):
            pass
        elif isinstance(action, MoveAction):
            pass
        elif isinstance(action, AffectAction):
            receivers = []
            for cell in action.cell:
                objects_in_cell = self.grid[cell]
                for obj in objects_in_cell:
                    if obj.id == action.sender and not action.selfcast:
                        continue
                    receivers.append(obj)
            pass



# damage / healing --> initiator, cell, meta
# moving           --> initiator, cell
# creation         --> initiat, cell
