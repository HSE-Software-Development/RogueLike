def diameter(graph: list[list[int]]) -> tuple[int, int]:

    def dfs(node: int, visited: set[int], depth: int) -> tuple[int, int]:
        visited.add(node)
        max_depth = depth
        farthest_node = node

        for neighbor in graph[node]:
            if neighbor not in visited:
                current_depth, current_farthest = dfs(neighbor, visited, depth + 1)
                if current_depth > max_depth:
                    max_depth = current_depth
                    farthest_node = current_farthest

        return max_depth, farthest_node

    _, res1 = dfs(0, set(), 0)
    _, res2 = dfs(res1, set(), 0)
    return res1, res2
