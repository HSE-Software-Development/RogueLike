def diameter(graph: list[list[int]]) -> list[int]:
    def dfs(node: int, visited: set[int], path: list[int]) -> tuple[int, list[int]]:
        visited.add(node)
        max_depth = len(path)
        farthest_path = path.copy()

        for neighbor in graph[node]:
            if neighbor not in visited:
                current_path = path + [neighbor]
                depth, current_farthest_path = dfs(neighbor, visited, current_path)
                if depth > max_depth:
                    max_depth = depth
                    farthest_path = current_farthest_path

        return max_depth, farthest_path

    _, path1 = dfs(0, set(), [0])
    _, path2 = dfs(path1[-1], set(), [path1[-1]])
    return path2
