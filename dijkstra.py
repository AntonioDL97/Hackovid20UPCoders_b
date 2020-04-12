from typing import List
from collections import deque

inf = float('inf')


class Edge:
    def __init__(self, start, end, cost):
        self.start = start
        self.end = end
        self.cost = cost


class Graph:
    def __init__(self, edges: List[Edge]):
        self.edges = edges
        self.vertices = set(sum(([edge.start, edge.end] for edge in self.edges), []))
        self.neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            self.neighbours[edge.start].add((edge.end, edge.cost))

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'

        # 1. Mark all nodes unvisited and store them.
        # 2. Set the distance to zero for our initial node
        # and to infinity for other nodes.
        distances = {vertex: inf for vertex in self.vertices}
        distances[source] = 0

        previous_vertices = {vertex: None for vertex in self.vertices}
        vertices = self.vertices.copy()

        while vertices:
            # 3. Select the unvisited node with the smallest distance,
            # it's current node now.
            current_vertex = min(vertices, key=lambda vertex: distances[vertex])

            # 6. Stop, if the smallest distance
            # among the unvisited nodes is infinity.
            if distances[current_vertex] == inf:
                break

            # 4. Find unvisited neighbors for the current node
            # and calculate their distances through the current node.
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost

                # Compare the newly calculated distance to the assigned
                # and save the smaller one.
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

            # 5. Mark the current node as visited
            # and remove it from the unvisited set.
            vertices.remove(current_vertex)

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return list(path), distances[dest]
