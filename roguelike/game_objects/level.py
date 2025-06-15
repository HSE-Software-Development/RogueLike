from roguelike.interfaces import *
from roguelike.types import Rect, Cell, Color
from enum import Enum
import random
from .room import Room
from roguelike.utils.mst import Graph
from roguelike.utils.bfs import bfs_shortest_path
from sklearn.cluster import KMeans
from typing import override, Optional
import numpy as np
from roguelike.game_objects.prey import Player
from roguelike.utils.diameter import diameter


class Level(ILevel, IGameObject):

    class LevelType(Enum):
        START = "start"
        FINISH = "finish"
        WITH_KEY = "with_key"
        COMMON = "common"

    def __init__(
        self,
        rect: Rect,
        level_type: LevelType = LevelType.COMMON,
        difficulty: float = 0.0,
    ):
        self.rect = rect
        self.difficulty = difficulty
        self.level_type = level_type
        self.player: Optional[Player] = None

    @override
    def on_init(self):
        b = 1.5
        k = self.difficulty - 0.5

        num_and_weight = [
            (3, b - k * 1.5),
            (4, b - k),
            (5, b - k),
            (6, b),
            (7, b + k),
            (8, b + k),
            (9, b + k * 1.5),
        ]

        self.num_of_rooms = random.choices(
            [num for num, _ in num_and_weight],
            weights=[weight for _, weight in num_and_weight],
            k=1,
        )[0]
        self.num_of_rooms = 7

        self.margin = 1
        self.rooms: list[Room] = []
        self.generate_rooms(self.num_of_rooms)

        self.connections: list[list[int]] = [[] for _ in range(len(self.rooms))]
        self.connect_rooms()

        self.set_entry_and_exit()

        # from roguelike.game_objects.prey import Player
        # from roguelike.game_objects.armor import Armor
        # from roguelike.game_objects.weapons import Weapon

        # self.rooms[0].add_object(
        #     Player(
        #         cell=self.rooms[0].rect.center,
        #         health=100,
        #         armor=Armor(cell=self.rooms[0].rect.center),
        #         weapon=Weapon(
        #             cell=self.rooms[0].rect.center
        #         ),  # Replace with actual weapon object
        #     )
        # )

    def set_entry_and_exit(self):
        u, v = diameter(self.connections)

        if self.rooms[u].rect.top < self.rooms[v].rect.top:
            self.entry_room = u
            self.exit_room = v
        else:
            self.entry_room = v
            self.exit_room = u

        visited = self.get_visited()
        entry_doors = self.get_doors(self.rooms[self.entry_room])
        random.shuffle(entry_doors)

        minY = 10000
        entry_door = Cell()
        for door in entry_doors:
            if door.y < minY:
                minY = door.y
                entry_door = door

        starts = []
        for x in range(entry_door.x - 1, entry_door.x + 2):
            for y in range(entry_door.y - 1, entry_door.y + 2):
                cell = Cell(x, y)
                visited[x][y] = True
                if (entry_door.x == x or entry_door.y == y) and self.rooms[
                    self.entry_room
                ].rect.is_outside(cell):
                    starts.append(Cell(x, y))
                self.all_doors_cells.append(cell)

        ends = [Cell(x, 1) for x in range(self.rect.left, self.rect.right + 1)]

        path = bfs_shortest_path(starts=starts, ends=ends, visited=visited)
        if path is not None:
            self.roads.append(path)

        self.rooms[self.entry_room].add_door(entry_door, -1, -1)

        visited = self.get_visited()
        exit_doors = self.get_doors(self.rooms[self.exit_room])

        random.shuffle(exit_doors)

        maxY = -10000
        exit_door = Cell()
        for door in exit_doors:
            if door.y > maxY:
                maxY = door.y
                exit_door = door

        starts = []
        for x in range(exit_door.x - 1, exit_door.x + 2):
            for y in range(exit_door.y - 1, exit_door.y + 2):
                cell = Cell(x, y)
                visited[x][y] = True
                if (exit_door.x == x or exit_door.y == y) and self.rooms[
                    self.exit_room
                ].rect.is_outside(cell):
                    starts.append(Cell(x, y))
                self.all_doors_cells.append(cell)

        ends = [
            Cell(x, self.rect.bottom - 1)
            for x in range(self.rect.left, self.rect.right + 1)
        ]

        path = bfs_shortest_path(starts=starts, ends=ends, visited=visited)
        if path is not None:
            self.roads.append(path)

        self.rooms[self.exit_room].add_door(exit_door, -1, 1)

    def no_collision(self, rect: Rect) -> bool:
        if not self.rect.with_margin(-1).is_inside(
            rect.lt
        ) or not self.rect.with_margin(-1).is_inside(rect.rb):
            return False

        for room in self.rooms:
            if rect.with_margin(margin=self.margin + 1).is_intersect(
                room.rect.with_margin(margin=self.margin + 1)
            ):
                return False
        return True

    def connect_rooms(self):
        gr = Graph(len(self.rooms))
        for i in range(len(self.rooms)):
            for j in range(i + 1, len(self.rooms)):
                weight = self.rooms[i].rect.center.distance(self.rooms[j].rect.center)
                gr.add_edge(i, j, weight)

        edges = gr.kruskal_mst()
        for u, v in edges:
            self.connections[u].append(v)
            self.connections[v].append(u)

        self.generate_roads(edges)

    def get_visited(self) -> dict[int, dict[int, bool]]:
        visited = {
            x: {y: False for y in range(self.rect.top, self.rect.bottom + 1)}
            for x in range(self.rect.left, self.rect.right + 1)
        }
        for x in range(self.rect.left, self.rect.right + 1):
            visited[x][self.rect.top] = True

        for x in range(self.rect.left, self.rect.right + 1):
            visited[x][self.rect.bottom] = True

        for y in range(self.rect.top, self.rect.bottom + 1):
            visited[self.rect.left][y] = True

        for y in range(self.rect.top, self.rect.bottom + 1):
            visited[self.rect.right][y] = True

        for room in self.rooms:
            rect = room.rect.with_margin(margin=self.margin)
            # rect = room.rect
            for x in range(rect.left, rect.right + 1):
                for y in range(rect.top, rect.bottom + 1):
                    visited[x][y] = True
        return visited

    def get_doors(self, room: Room) -> list[Cell]:
        doors = []
        for x in range(room.rect.left + 3, room.rect.right - 3 + 1):
            doors.append(Cell(x, room.rect.top))
            doors.append(Cell(x, room.rect.bottom))
        for y in range(room.rect.top + 3, room.rect.bottom - 3 + 1):
            doors.append(Cell(room.rect.left, y))
            doors.append(Cell(room.rect.right, y))

        doors = [door for door in doors if door not in self.all_doors_cells]
        return doors

    def generate_roads(self, edges: list[tuple[int, int]]):
        self.roads = []

        self.all_doors_cells: list[Cell] = []

        def get_nearest_doors(room1: Room, room2: Room) -> tuple[Cell, Cell]:
            doors1 = self.get_doors(room1)
            doors2 = self.get_doors(room2)

            minDist = 10000
            res1: Cell = Cell()
            res2: Cell = Cell()
            for door1 in doors1:
                for door2 in doors2:
                    if door1.distance(door2) < minDist:
                        minDist = door1.distance(door2)
                        res1 = door1
                        res2 = door2

            return (res1, res2)

        for u, v in edges:
            room_u = self.rooms[u]
            room_v = self.rooms[v]

            visited = self.get_visited()

            door1, door2 = get_nearest_doors(room_u, room_v)
            len_room_u = len(room_u.doors)
            len_room_v = len(room_v.doors)
            room_u.add_door(door1, v, len_room_v)
            room_v.add_door(door2, u, len_room_u)

            starts = []
            for x in range(door1.x - 1, door1.x + 2):
                for y in range(door1.y - 1, door1.y + 2):
                    cell = Cell(x, y)
                    visited[x][y] = True
                    if (door1.x == x or door1.y == y) and room_u.rect.is_outside(cell):
                        starts.append(Cell(x, y))
                    self.all_doors_cells.append(cell)

            ends = []
            for x in range(door2.x - 1, door2.x + 2):
                for y in range(door2.y - 1, door2.y + 2):
                    cell = Cell(x, y)
                    visited[x][y] = True
                    if (door2.x == x or door2.y == y) and room_v.rect.is_outside(cell):
                        ends.append(Cell(x, y))
                        visited[x][y] = False
                    self.all_doors_cells.append(cell)

            path = bfs_shortest_path(starts, ends, visited)
            print(f"Path from {door1} to {door2}: {path}")
            if path is not None:
                self.roads.append(path)

    def generate_rooms(self, num_of_rooms: int):
        self.points = []
        for _ in range(num_of_rooms * 3):
            rect = self.rect.with_margin(-5)
            x = random.randint(rect.left, rect.right)
            y = random.randint(rect.top, rect.bottom)
            self.points.append([x, y])

        print(f"Points: {self.points}")
        print(f"Number of rooms: {num_of_rooms}")
        print(self.rect)

        kmeans = KMeans(n_clusters=num_of_rooms, random_state=0).fit(self.points)
        kmeans.fit(np.array(self.points))
        self.centers = [
            [int(center[0]), int(center[1])] for center in kmeans.cluster_centers_
        ]
        print(f"Centers: {self.centers}")

        max_width = int(self.rect.width / 2.5)
        min_width = max(self.rect.width // 10, 5)
        max_height = int(self.rect.height / 2.5)
        min_height = max(self.rect.height // 10, 4)
        max_tries = 50
        for center in self.centers:
            for t in range(max_tries):
                if t < 4:
                    width = random.randint(min_width, max_width)
                    height = random.randint(min_height, max_height)
                else:
                    center[0] = random.randint(self.rect.left + 1, self.rect.right - 1)
                    center[1] = random.randint(
                        self.rect.top + 1,
                        self.rect.bottom - 1,
                    )
                    width = random.randint(min_width, max_width)
                    height = random.randint(min_height, max_height)

                lt = Cell(center[0] - width // 2, center[1] - height // 2)
                rb = Cell(center[0] + width // 2, center[1] + height // 2)
                rect = Rect(lt=lt, rb=rb)

                if self.no_collision(rect):
                    room = Room(rect=rect)
                    room.set_index(len(self.rooms))
                    self.rooms.append(room)
                    break
                else:
                    print(f"Collision detected for room at {center}, retrying...")
        print(f"Generated rooms: {len(self.rooms)}")

    @override
    def on_draw(self, animation: IAnimation):

        # animation.print(self.num_of_rooms)
        for room in self.rooms:
            room.on_draw(animation)

        # for x in range(self.rect.left, self.rect.right + 1):
        #     animation.draw(
        #         Cell(x, self.rect.top), " ", color=Color.BLACK_YELLOW, z_buffer=0
        #     )

        # for x in range(self.rect.left, self.rect.right + 1):
        #     animation.draw(
        #         Cell(x, self.rect.bottom), " ", color=Color.BLACK_YELLOW, z_buffer=0
        #     )

        # for y in range(self.rect.top, self.rect.bottom + 1):
        #     animation.draw(
        #         Cell(self.rect.left, y), " ", color=Color.BLACK_YELLOW, z_buffer=0
        #     )

        # for y in range(self.rect.top, self.rect.bottom + 1):
        #     animation.draw(
        #         Cell(self.rect.right, y), " ", color=Color.BLACK_YELLOW, z_buffer=0
        #     )

        # for center in self.centers:
        #     animation.draw(Cell(center[0], center[1]), "C", color=Color.RED, z_buffer=2)

        for road in self.roads:
            for point in road:
                animation.draw(point, " ", color=Color.BLACK_GREEN, z_buffer=5)
        # for point in self.points:
        #     animation.draw(Cell(point[0], point[1]), "P", z_buffer=2)

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        actions: list[IGameAction] = []
        for room in self.rooms:
            actions.extend(room.on_update(keyboard))

        for action in actions:
            if isinstance(action, ILevelGameAction):
                action.level_handler(self)

        return actions

    def set_player(self, player: Player):
        self.player = player
        self.rooms[self.entry_room].set_player(player, -1)

    @override
    def move_player(self, prev_room: int, next_room: int, door_index: int):
        if self.player is None:
            return

        self.rooms[prev_room].remove_player(self.player)
        self.rooms[next_room].set_player(self.player, door_index)

    @override
    def remove_player(self, room_index: int):
        if self.player is None:
            return
        self.rooms[room_index].remove_player(self.player)
        self.player = None
