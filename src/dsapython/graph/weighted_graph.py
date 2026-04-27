import math
from typing import Any

from unweightedgraph import Vertex


def find_unvisited_vertex_with_min_distance(distance, visited_vertex: set[Vertex]) -> Any | None:
    min_vertex = None
    min_distance = math.inf
    for v in distance:
        if v not in visited_vertex:
            if distance[v] < min_distance:
                min_distance = distance[v]
                min_vertex = v
    return min_vertex


class WeightedGraph:
    def __init__(self, name):
        self.name = name
        self.graph_view: dict[Vertex, list[tuple[Vertex, int]]] = {}

    def _add_vertex(self, vertex: Vertex):
        if vertex not in self.graph_view:
            self.graph_view[vertex] = []

    def add_edge(self, vertex1: Vertex, vertex2: Vertex, weight: int):
        self._add_vertex(vertex1)
        self._add_vertex(vertex2)
        vertex1.out_degree += 1
        vertex2.in_degree += 1
        self.graph_view[vertex1].append((vertex2, weight))

    def add_edges(self, vertex1: Vertex, vertex: list[tuple[Vertex, int]]):
        for ver, wight in vertex:
            self.add_edge(vertex1, ver, wight)

    def single_source_sortest_path_dijkstra_algorithm(self, start: Vertex):
        distance = {}
        visited_vertex = set()
        for vertex in self.graph_view.keys():
            distance[vertex] = math.inf
        distance[start] = 0
        while len(visited_vertex) != len(self.graph_view.keys()):
            if start is None:  # Stop if no more reachable nodes
                break
            visited_vertex.add(start)
            self.update_neighbour_distance(start, distance, visited_vertex)
            start = find_unvisited_vertex_with_min_distance(distance, visited_vertex)

    def update_neighbour_distance(self, vertex: Vertex, distance, visited: set[Vertex]):
        for vert, wight in self.graph_view[vertex]:
            if vert not in visited:
                distance[vert] = min(distance[vertex] + wight, distance[vert])

    def bellman_ford_algorithm(self, start: Vertex):
        distance = {}
        for vertex in self.graph_view.keys():
            distance[vertex] = math.inf
        distance[start] = 0
        for _ in range(len(self.graph_view.keys()) - 1):
            for vertex in self.graph_view.keys():
                for vert, wight in self.graph_view[vertex]:
                    distance[vert] = min(distance[vertex] + wight, distance[vert])
        for u in self.graph_view:
            for v, weight in self.graph_view[u]:
                if distance[u] != math.inf and distance[u] + weight < distance[v]:
                    print("Error: Graph contains a Negative Weight Cycle!")
                    return None
        return distance

    def floyd_warshall_algorithm(self, graph):
        # 1. Saari unique vertices collect karo (Source + Destination dono)
        all_nodes = set(self.graph_view.keys())
        for neighbours in self.graph_view.values():
            for v, weight in neighbours:
                all_nodes.add(v)

        vertices = list(all_nodes)
        n = len(vertices)
        v_to_idx = {vertex: i for i, vertex in enumerate(vertices)}

        # 2. Distance matrix initialize karo
        dist = [[math.inf] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0

        # 3. Direct edges fill karo
        for u in self.graph_view:
            for v, weight in self.graph_view[u]:
                dist[v_to_idx[u]][v_to_idx[v]] = weight

        # 4. Triple loop logic
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    # Check: Kya i->k aur k->j dono paths exist karte hain?
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return dist, vertices