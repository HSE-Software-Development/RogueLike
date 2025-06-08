from .room import Room
from typing import override
from enum import Enum
from roguelike.types import Cell, Rect, Animation, GameObject, Color
from sklearn.cluster import KMeans
from roguelike.utils.mst import Graph
from roguelike.utils.bfs import bfs_shortest_path
from .example_object import ExampleObject
import random
import numpy as np


class Level(GameObject):
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

    def no_collision(self, rect: Rect) -> bool:
        if not self.rect.is_inside(rect.lt) or not self.rect.is_inside(rect.rb):
            return False

        for room in self.rooms:
            if rect.with_margin(margin=self.margin + 1).is_intersect(
                room.rect.with_margin(margin=self.margin + 1)
            ):
                return False
        return True

    def init(self):
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
        self.num_of_rooms = 10

        self.margin = 1
        self.rooms: list[Room] = []
        self.generate_rooms(self.num_of_rooms)
        self.connections: dict[int, list[int]] = {}
        self.connect_rooms()

        self.rooms[0].add_object(ExampleObject(position=self.rooms[0].rect.center))

    def connect_rooms(self):
        gr = Graph(len(self.rooms))
        for i in range(len(self.rooms)):
            for j in range(i + 1, len(self.rooms)):
                weight = self.rooms[i].rect.center.distance(self.rooms[j].rect.center)
                gr.add_edge(i, j, weight)

        edges = gr.kruskal_mst()
        for u, v in edges:
            if u not in self.connections:
                self.connections[u] = []
            if v not in self.connections:
                self.connections[v] = []
            self.connections[u].append(v)
            self.connections[v].append(u)

        self.generate_roads(edges)

    def generate_roads(self, edges: list[tuple[int, int]]):
        self.roads = []

        def get_nearest_door(room1: Room, room2: Room) -> Cell:
            center = room2.rect.center
            doors = [
                Cell(room1.rect.center.x, room1.rect.top),
                Cell(room1.rect.center.x, room1.rect.bottom),
                Cell(room1.rect.left, room1.rect.center.y),
                Cell(room1.rect.right, room1.rect.center.y),
            ]

            return min(doors, key=lambda door: door.distance(center))

        for u, v in edges:
            room_u = self.rooms[u]
            room_v = self.rooms[v]

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

            door1 = get_nearest_door(room_u, room_v)
            room_u.add_door(door1)
            starts = []
            for x in range(door1.x - 1, door1.x + 2):
                for y in range(door1.y - 1, door1.y + 2):
                    visited[x][y] = True
                    starts.append(Cell(x, y))

            door2 = get_nearest_door(room_v, room_u)
            room_v.add_door(door2)
            ends = []
            for x in range(door2.x - 1, door2.x + 2):
                for y in range(door2.y - 1, door2.y + 2):
                    visited[x][y] = False
                    ends.append(Cell(x, y))

            path = bfs_shortest_path(starts, ends, visited)
            print(f"Path from {door1} to {door2}: {path}")
            if path is not None:
                self.roads.append(path)

    def generate_rooms(self, num_of_rooms: int):
        self.points = []
        for _ in range(num_of_rooms * 4):
            x = random.randint(self.rect.left, self.rect.right)
            y = random.randint(self.rect.top, self.rect.bottom)
            self.points.append([x, y])
        print(f"Points: {self.points}")
        print(f"Number of rooms: {num_of_rooms}")
        print(self.rect)

        kmeans = KMeans(n_clusters=num_of_rooms, random_state=0).fit(self.points)
        kmeans.fit(np.array(self.points))
        self.centers = [
            (int(center[0]), int(center[1])) for center in kmeans.cluster_centers_
        ]
        print(f"Centers: {self.centers}")

        max_width = int(self.rect.width / 2.5)
        min_width = max(self.rect.width // 10, 6)
        max_height = int(self.rect.height / 2.5)
        min_height = max(self.rect.height // 10, 8)
        max_tries = 20
        for center in self.centers:
            for _ in range(max_tries):
                width = random.randint(min_width, max_width)
                height = random.randint(min_height, max_height)
                lt = Cell(center[0] - width // 2, center[1] - height // 2)
                rb = Cell(center[0] + width // 2, center[1] + height // 2)
                rect = Rect(lt=lt, rb=rb)

                if self.no_collision(rect):
                    room = Room(rect=rect)
                    self.rooms.append(room)
                    break
                else:
                    print(f"Collision detected for room at {center}, retrying...")
        print(f"Generated rooms: {len(self.rooms)}")

    @override
    def on_draw(self, animation: Animation):

        # animation.print(self.num_of_rooms)
        for room in self.rooms:
            room.on_draw(animation)

        for x in range(self.rect.left, self.rect.right + 1):
            animation.draw(Cell(x, self.rect.top), "#", z_buffer=0)

        for x in range(self.rect.left, self.rect.right + 1):
            animation.draw(Cell(x, self.rect.bottom), "#", z_buffer=0)

        for y in range(self.rect.top, self.rect.bottom + 1):
            animation.draw(Cell(self.rect.left, y), "#", z_buffer=0)

        for y in range(self.rect.top, self.rect.bottom + 1):
            animation.draw(Cell(self.rect.right, y), "#", z_buffer=0)

        # for center in self.centers:
        #     animation.draw(Cell(center[0], center[1]), "C", z_buffer=2)

        for road in self.roads:
            for point in road:
                animation.draw(point, "@", color=Color.GREEN, z_buffer=1)
        # for point in self.points:
        #     animation.draw(Cell(point[0], point[1]), "P", z_buffer=2)

    @override
    def on_update(self):
        for room in self.rooms:
            room.on_update()
