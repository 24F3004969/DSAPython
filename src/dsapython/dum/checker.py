from collections import deque


def countVertexVisit(graph, start_vertex, total_tanks_count):
    if start_vertex is None:
        return 0
    queue = deque([start_vertex])
    visited = {start_vertex}

    while queue:
        curr = queue.popleft()
        for neighbor in graph.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited)


def findMasterTank(tanks, pipes):
    if not tanks:
        return 0

    adj = {t: [] for t in tanks}
    for u, v in pipes:
        adj[u].append(v)

    visited = set()
    last_finished_node = tanks[0]

    # Step 1: DFS to find the candidate for master tank
    def dfs(u):
        visited.add(u)
        for neighbor in adj.get(u, []):
            if neighbor not in visited:
                dfs(neighbor)

    for tank in tanks:
        if tank not in visited:
            dfs(tank)
            # The last node that finishes a DFS traversal is the best candidate
            last_finished_node = tank

    # Step 2: Verify if the candidate can actually reach all other tanks
    if countVertexVisit(adj, last_finished_node, len(tanks)) == len(tanks):
        return last_finished_node

    return 0


# --- Test Case Execution ---
tanks_list = [1, 2, 3, 4]
pipes_list = [(1, 2), (2, 3), (3, 4)]  # Simple path: 1 -> 2 -> 3 -> 4

result = findMasterTank(tanks_list, pipes_list)
print(f"Master Tank Found: {result}")
