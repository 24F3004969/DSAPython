class Vertex:
    def __init__(self, data: str):
        self.data = data

    def __repr__(self) -> str:
        return f"Vertex({self.data!r})"

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
        self.graph_view[vertex1].append(vertex2)

    def add_edges(self, vertex1: Vertex, vertex: list[Vertex]):
        for ver in vertex:
            self.add_edge(vertex1, ver)

    def bfs(self, start: Vertex):
        visited = {}
        queue = []
        for x in self.graph_view.keys():
            visited[x] = -1
        queue.append(start)
        while len(queue) != 0:
            vertex = queue.pop(0)
            if visited[vertex] == -1:
                visited[vertex] = vertex
            vr = self.graph_view[vertex]
            for x in vr:
                if x is not queue:
                    queue.append(x)

        return visited

    def _find_neighbour(self, vertex: Vertex, visited: dict[Vertex, bool]) -> Vertex | None:
        neighbour = self.graph_view[vertex]
        for x in neighbour:
            if not visited[x]:
                return x
        return None

    def dfs(self, start: Vertex):
        visited = {}
        stack = []
        for x in self.graph_view.keys():
            visited[x] = False
        init = start
        tem = self._find_neighbour(init, visited)
        if tem is not None:
            stack.append(init)
        visited[init] = True
        init = tem
        while len(stack) != 0:
            visited[init] = True
            tem = self._find_neighbour(init, visited)
            if tem is not None:
                stack.append(init)
                init = tem
            else:
                init = stack.pop()
                tem = self._find_neighbour(init, visited)
                if tem is not None:
                    stack.append(init)
                    init = tem
        return visited


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

    # 3. Run BFS
    print(f"Starting BFS on {my_graph.name} from Vertex {v_a}:")
    traversal_order = my_graph.dfs(v_a)
    print(traversal_order)
    for vertex in traversal_order.keys():
        if traversal_order[vertex]:
            print(f"Visited: {vertex}")


if __name__ == "__main__":
    main()
