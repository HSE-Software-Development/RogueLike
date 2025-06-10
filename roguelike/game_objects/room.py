from roguelike.types import Cell, Rect
from typing import override
from roguelike.types import Animation, GameObject, GameAction, Color
from roguelike.keyboard import pressed


class Room(GameObject):

    def __init__(self, rect: Rect):
        self.objects: list[GameObject] = []
        self.actions: list[GameAction] = []
        self.rect = rect
        self.doors: list[Cell] = []

    @override
    def init(self):
        pass

    @override
    def on_draw(self, animation: Animation):
        # if "k" in pressed():
        #     animation.print("K")
        # else:
        #     animation.print("_")

        for x in range(self.rect.left, self.rect.right + 1):
            animation.draw(Cell(x, self.rect.top), "*", color=Color.PURPLE, z_buffer=1)

        for x in range(self.rect.left, self.rect.right + 1):
            animation.draw(
                Cell(x, self.rect.bottom), "*", color=Color.PURPLE, z_buffer=1
            )

        for y in range(self.rect.top, self.rect.bottom + 1):
            animation.draw(Cell(self.rect.left, y), "*", color=Color.PURPLE, z_buffer=1)

        for y in range(self.rect.top, self.rect.bottom + 1):
            animation.draw(
                Cell(self.rect.right, y), "*", color=Color.PURPLE, z_buffer=1
            )

        for x in range(self.rect.left + 1, self.rect.right):
            for y in range(self.rect.top + 1, self.rect.bottom):
                animation.draw(Cell(x, y), ".", z_buffer=0)

        for obj in self.objects:
            if not obj.is_deleted:
                obj.on_draw(animation)

        # for door in self.doors:
        #     for x in range(door.x - 1, door.x + 2):
        #         for y in range(door.y - 1, door.y + 2):
        #             animation.draw(Cell(x, y), "D", z_buffer=2)

    def validate_cell(self, cell: Cell) -> bool:
        return self.rect.is_inside(cell)

    def add_object(self, object: GameObject) -> bool:
        if not self.validate_cell(object.cell):
            return False
        self.objects.append(object)

    def add_door(self, cell: Cell) -> bool:
        return self.doors.append(cell)

    @override
    def on_update(self):
        for obj in self.objects:
            if not obj.is_deleted:
                self.actions.extend(obj.on_update())

        new_actions: list[GameAction] = []
        for action in self.actions:
            new_actions.extend(action.execute(self))
            # new_actions.extend(self.execute_action(action))
        self.actions = new_actions

        return new_actions
