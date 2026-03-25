def get_adj_list(tanks, pipes):
    adj = {tank: [] for tank in tanks}
    for u, v in pipes:
        adj[u].append(v)
    return adj


def find_candidate(adj, tanks):
    visited = set()
    last_node = 0

    def dfs(u):
        visited.add(u)
        for v in adj[u]:
            if v not in visited:
                dfs(v)
        nonlocal last_node
        last_node = u  # The node that finishes last

    for tank in tanks:
        if tank not in visited:
            dfs(tank)
    return last_node


from collections import deque


def get_reachable_count(adj, start_node):
    if not start_node:
        return 0

    queue = deque([start_node])
    visited = {start_node}

    while queue:
        curr = queue.popleft()  # O(1) time
        for neighbor in adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited)


def findMasterTank(tanks, pipes):
    # Step 1: Format the data
    adj = get_adj_list(tanks, pipes)

    # Step 2: Find the ONLY potential candidate
    candidate = find_candidate(adj, tanks)

    # Step 3: Check if that candidate can actually reach everyone
    if get_reachable_count(adj, candidate) == len(tanks):
        return candidate

    return 0
