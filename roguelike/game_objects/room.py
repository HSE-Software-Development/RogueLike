import random
import time
from roguelike.game_objects.prey.based_hater import BasedHater
from roguelike.interfaces import *
from roguelike.types import Cell, Rect, Color
from typing import override, Optional
from roguelike.game_objects.prey import Player
from roguelike.game_actions import ChangeRoomAction, ChangeLevelAction
from enum import Enum


class RoomType(Enum):
    MAINQUEST = "main_quest"
    SIDEQUEST = "side_quest"


class Room(IRoom, IGameObject):

    def __init__(self, rect: Rect):
        self.objects: list[IGameObjectWithPosition] = []
        self.rect = rect
        self.doors: list[tuple[Cell, int, int]] = []

        self.player: Optional[Player] = None
        self.flage = True

        self.update_time = 20.0  # per second
        self.previous_time = -1.0
        self.room_type: RoomType = RoomType.MAINQUEST
        self.difficulty: float = 0.0

    def set_difficulty(self, difficulty: float):
        self.difficulty = difficulty

    def set_index(self, index: int):
        self.index = index

    def set_type(self, room_type: RoomType):
        self.room_type = room_type

    def add_door(self, cell: Cell, next_room_index: int, door_index: int):
        self.doors.append((cell, next_room_index, door_index))

    def set_player(self, player: Player, door_index: int):
        self.player = player

        door, _, _ = self.doors[door_index]
        for x in range(door.x - 1, door.x + 2):
            for y in range(door.y - 1, door.y + 2):
                cell = Cell(x, y)
                if (y == door.y or x == door.x) and self.validate_cell(cell):
                    self.player.cell = cell

        self.flag = False
        self.add_object(player)

    def remove_player(self, player: Player):
        self.player = None
        self.remove_object(player)

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
    def on_init(self):
        for _ in range(0, 5):
            cell = Cell(
                random.randint(self.rect.lt.x + 1, self.rect.rb.x - 1),
                random.randint(self.rect.lt.y + 1, self.rect.rb.y - 1),
            )
            print(str(cell.x) + " " + str(cell.y))
            self.objects.append(BasedHater(health=10, cell=cell))

    @override
    def on_draw(self, animation: IAnimation):
        # if "k" in pressed():
        #     animation.print("K")
        # else:
        #     animation.print("_")

        color = (
            Color.BLACK_PURPLE
            if self.room_type == RoomType.MAINQUEST
            else Color.BLACK_YELLOW
        )

        for x in range(self.rect.left, self.rect.right + 1):
            animation.draw(Cell(x, self.rect.top), " ", color=color, z_buffer=1)

        for x in range(self.rect.left, self.rect.right + 1):
            animation.draw(Cell(x, self.rect.bottom), " ", color=color, z_buffer=1)

        for y in range(self.rect.top, self.rect.bottom + 1):
            animation.draw(Cell(self.rect.left, y), " ", color=color, z_buffer=1)

        for y in range(self.rect.top, self.rect.bottom + 1):
            animation.draw(Cell(self.rect.right, y), " ", color=color, z_buffer=1)

        for x in range(self.rect.left + 1, self.rect.right):
            for y in range(self.rect.top + 1, self.rect.bottom):
                animation.draw(Cell(x, y), " ", z_buffer=0)

        for door, _, _ in self.doors:
            for x in range(door.x - 1, door.x + 2):
                for y in range(door.y - 1, door.y + 2):
                    if self.rect.is_on_edge(Cell(x, y)):
                        animation.draw(Cell(x, y), "@", color=Color.GREEN, z_buffer=2)

        for obj in self.objects:
            obj.on_draw(animation)

        # for door in self.doors:
        #     for x in range(door.x - 1, door.x + 2):
        #         for y in range(door.y - 1, door.y + 2):
        #             animation.draw(Cell(x, y), "D", z_buffer=2)

    @override
    def validate_cell(self, cell: Cell) -> bool:
        return self.rect.is_inside(cell)

    @override
    def add_object(self, object: IGameObjectWithPosition):
        if not self.validate_cell(object.cell):
            return
        self.objects.append(object)

    @override
    def remove_object(self, object: IGameObjectWithPosition):
        self.objects = [obj for obj in self.objects if obj != object]

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        if not self.is_update_time():
            return []

        actions = []
        for obj in self.objects:
            actions.extend(obj.on_update(keyboard))

        for action in actions:
            if isinstance(action, IRoomGameAction):
                action.room_handler(self)

        if self.player is not None:
            player_cells = []
            if keyboard.is_pressed("w"):
                player_cells.append(Cell(self.player.cell.x, self.player.cell.y - 1))
            if keyboard.is_pressed("s"):
                player_cells.append(Cell(self.player.cell.x, self.player.cell.y + 1))
            if keyboard.is_pressed("a"):
                player_cells.append(Cell(self.player.cell.x - 1, self.player.cell.y))
            if keyboard.is_pressed("d"):
                player_cells.append(Cell(self.player.cell.x + 1, self.player.cell.y))

            for door, room_index, door_index in self.doors:
                for x in range(door.x - 1, door.x + 2):
                    for y in range(door.y - 1, door.y + 2):
                        cell = Cell(x, y)
                        if self.rect.is_on_edge(cell):
                            if cell in player_cells:
                                if self.flag:
                                    if room_index == -1:
                                        if door_index != -1:
                                            actions.append(
                                                ChangeLevelAction(
                                                    room_index=self.index,
                                                )
                                            )
                                    else:
                                        actions.append(
                                            ChangeRoomAction(
                                                prev_room=self.index,
                                                next_room=room_index,
                                                door_index=door_index,
                                            )
                                        )
                                self.flag = True

        return actions
