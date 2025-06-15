from collections import deque
from roguelike.types import Cell
import random


def bfs_shortest_path(
    starts: list[Cell], ends: list[Cell], visited: dict[int, dict[int, bool]]
) -> list[Cell] | None:

    queue = deque()
    for start in starts:
        queue.append([start])

    for start in starts:
        visited[start.x][start.y] = True

    cnt = 0
    while queue:
        cnt += 1
        path = queue.popleft()
        node = path[-1]
        print(path, starts, ends)
        if node in ends:
            return path

        dlts = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(dlts)
        for dlt in dlts:
            neighbor = Cell(node.x + dlt[0], node.y + dlt[1])

            if not (
                0 <= neighbor.x < len(visited) and 0 <= neighbor.y < len(visited[0])
            ):
                continue

            if visited[neighbor.x][neighbor.y]:
                continue

            new_path = list(path)
            new_path.append(neighbor)

            for cell in ends:
                if neighbor == cell:
                    return new_path

            queue.append(new_path)
            visited[neighbor.x][neighbor.y] = True

    return None
