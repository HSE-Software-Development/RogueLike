import random
import time
from roguelike.game_objects.armor.old_robe import BronzeArmor
from roguelike.game_objects.prey.based_hater import BasedHater
from roguelike.game_objects.weapons.range_weapons.wood_bow import StrongBow
from roguelike.interfaces import *
from roguelike.interfaces.item_types import ItemType
from roguelike.types import Cell, Rect, Color
from typing import override, Optional
from roguelike.game_objects.prey import Player
from roguelike.game_objects.key import Key
from roguelike.game_actions import ChangeRoomAction, ChangeLevelAction, PickedKey
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

        self.room_type: RoomType = RoomType.MAINQUEST
        self.difficulty: float = 0.0
        self.key: Optional[Key] = None

    def add_key(self):
        self.key = Key(cell=self.rect.center)
        self.add_object(self.key)

    def remove_key(self):
        if self.key != None and self.player != None:
            for item in self.player.inventory.items:
                if item != None and item.type == ItemType.KEY:
                    self.player.inventory.items.remove(item)
                    break
            self.remove_object(self.key)
            self.key = None

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
                    for child in self.player.children:
                        child.cell = cell

        self.flag = False
        self.add_object(player)

    def remove_player(self, player: Player):
        self.player = None
        self.remove_object(player)

    @override
    def on_init(self):
        if self.room_type == RoomType.SIDEQUEST:
            cell = Cell(
                random.randint(self.rect.lt.x + 1, self.rect.rb.x - 1),
                random.randint(self.rect.lt.y + 1, self.rect.rb.y - 1),
            )
            self.objects.append(StrongBow(cell))
            cell = Cell(
                random.randint(self.rect.lt.x + 1, self.rect.rb.x - 1),
                random.randint(self.rect.lt.y + 1, self.rect.rb.y - 1),
            )
            self.objects.append(BronzeArmor(cell))
        for _ in range(0, max(int(self.difficulty * 6), 1)):
            cell = Cell(
                random.randint(self.rect.lt.x + 1, self.rect.rb.x - 1),
                random.randint(self.rect.lt.y + 1, self.rect.rb.y - 1),
            )
            self.objects.append(BasedHater(cell, 10, self.difficulty))

    @override
    def on_draw(self, animation: IAnimation):
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

        if self.player is not None and self.key is not None:
            if (
                self.player.cell == self.key.cell
                or self.player.cell == self.key.cell + Cell(0, -1)
            ):
                actions.append(PickedKey(self.index))

        return actions
