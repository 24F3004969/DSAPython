import time
from collections import deque


class Vertex:
    __slots__ = ("data", "in_degree", "out_degree")

    def __init__(self, data: str):
        self.data = data
        self.in_degree = 0  # now public
        self.out_degree = 0  # now public

    def __repr__(self) -> str:
        return (f"Vertex(data={self.data !r}, "
                f"in_degree={self.in_degree!r}, "
                f"out_degree={self.out_degree!r})")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vertex):
            return NotImplemented
        return self.data == other.data

    def __hash__(self) -> int:
        return hash(self.data)


class Graph:
    graph_view = {}

    def __init__(self, name: str):
        self.name = name

    def _add_vertex(self, vertex: Vertex):
        if vertex not in self.graph_view:
            self.graph_view[vertex] = []

    def add_edge(self, vertex1: Vertex, vertex2: Vertex):
        self._add_vertex(vertex1)
        self._add_vertex(vertex2)
        vertex1.out_degree += 1
        vertex2.in_degree += 1
        self.graph_view[vertex1].append(vertex2)

    def add_edges(self, vertex1: Vertex, vertex: list[Vertex]):
        for ver in vertex:
            self.add_edge(vertex1, ver)

    def bfs(self, start: Vertex):
        visited = set()
        path = {start: start}
        queue = deque([])
        queue.append(start)
        while len(queue) != 0:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
            vr = self.graph_view[vertex]
            for x in vr:
                if x not in visited:
                    queue.append(x)
                    path[x] = vertex
        return path

    def dfs(self, start: Vertex):
        visited: set[Vertex] = set()
        stack: list[Vertex] = [start]
        path = {start: start}
        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
            for nbr in self.graph_view.get(v):
                if nbr not in visited:
                    stack.append(nbr)
                    path[nbr] = v

        return visited, path

    def dfs_recursive(self, u, visited, path):
        if u in visited:
            return path
        visited.add(u)
        for v in self.graph_view[u]:
            if v not in visited:
                path[v] = u
                self.dfs_recursive(v, visited, path)
        return path

    def dfs_iterative(self, start):
        """
        Iterative DFS that returns a parent map (node -> parent).
        The start node has parent None.
        """
        visited = set()
        parent = {start: None}
        stack = [start]

        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)

            for v in self.graph_view.get(u, []):
                if v not in visited and v not in parent:
                    parent[v] = u
                    stack.append(v)

        return parent, visited

    def find_component(self):
        components: dict[int, list[Vertex]] = {}
        comp_id = 0
        i_vertex = min(self.graph_view.keys(), key=lambda x: x.data)
        index_visited = 0
        max_index = len(self.graph_view)
        l_v_v = []
        while index_visited < max_index:
            visited = self.dfs_iterative(i_vertex)[1]
            index_visited = index_visited + len(visited)
            if len(visited) > 0:
                k = list(visited)
                components[comp_id] = k
                l_v_v += k
                comp_id += 1
            diff = set(self.graph_view.keys()) - set(l_v_v)
            if len(diff) > 0:
                i_vertex = min(diff, key=lambda x: x.data)
        return components

    def _find_component(self) -> dict[int, list[Vertex]]:
        components: dict[int, list[Vertex]] = {}
        unvisited: set[Vertex] = set(self.graph_view.keys())  # all vertices in the graph
        comp_id = 0

        while unvisited:
            # Start from the lexicographically smallest unvisited vertex (by .data)
            start = min(unvisited, key=lambda v: v.data)

            # Run your DFS and keep only the vertices actually reached (True)
            reached_map = self.dfs(start)  # expected: dict[Vertex, bool]
            reached: set[Vertex] = {v for v, seen in reached_map.items() if seen}

            # Record this component (sorted for stable output, optional)
            components[comp_id] = sorted(reached, key=lambda v: v.data)

            # Remove reached from the pool; loop until nothing remains
            unvisited -= reached
            comp_id += 1

        return components

    def topological_sort(self):
        in_degree = {k: k.in_degree for k in self.graph_view.keys()}
        print(in_degree)


def main():
    # 1. Initialize Vertices
    v_a = Vertex("A")
    v_b = Vertex("B")
    v_c = Vertex("C")
    v_d = Vertex("D")
    v_e = Vertex("E")
    v_f = Vertex("F")
    v_g = Vertex("G")

    # 2. Create Graph
    my_graph = Graph("Large Network")

    # 3. Add Multiple Edges (Creating a layered structure)
    # Root connections
    my_graph.add_edge(v_a, v_b)
    my_graph.add_edge(v_a, v_c)

    # Mid-layer connections
    my_graph.add_edge(v_b, v_d)
    my_graph.add_edge(v_b, v_e)
    my_graph.add_edge(v_c, v_f)

    # Cross-connections and Sink
    my_graph.add_edge(v_d, v_g)
    my_graph.add_edge(v_e, v_g)
    my_graph.add_edge(v_f, v_g)
    my_graph.add_edge(v_c, v_e)  # Extra link between branches
    print(my_graph.graph_view)
    # 3. Run BFS
    print(f"Starting BFS on {my_graph.name} from Vertex {v_a}:")
    print(my_graph.bfs(v_a))
    traversal_order = my_graph.dfs_recursive(v_a, set(), dict())
    print(traversal_order)
    print(my_graph.dfs_iterative(v_a))
    start_time = time.perf_counter()
    print(my_graph.find_component())
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.4f} seconds")
    my_graph.topological_sort()
    #
    # for vertex in traversal_order.keys():
    #     if traversal_order[vertex]:
    #         print(f"Visited: {vertex}")


if __name__ == "__main__":
    main()
