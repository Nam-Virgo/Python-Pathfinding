# modules/graph.py

import math

class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.visited = False

    def get_other_node(self, node):
        return self.node2 if node == self.node1 else self.node1

    @property
    def weight(self):
        return math.hypot(
            self.node1.latitude - self.node2.latitude,
            self.node1.longitude - self.node2.longitude
        )


class Node:
    def __init__(self, id, latitude, longitude):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.edges = []
        self.visited = False
        self.reset()

    def connect_to(self, other_node):
        edge = Edge(self, other_node)
        self.edges.append(edge)
        other_node.edges.append(edge)

    @property
    def neighbors(self):
        return [
            {"node": edge.get_other_node(self), "edge": edge}
            for edge in self.edges
        ]

    @property
    def total_distance(self):
        return self.distance_from_start + self.distance_to_end

    def reset(self):
        self.visited = False
        self.distance_from_start = 0
        self.distance_to_end = 0
        self.parent = None
        self.referer = None
        for neighbor in self.neighbors:
            neighbor["edge"].visited = False


class Graph:
    def __init__(self):
        self.nodes = {}
        self.start_node = None

    def add_node(self, id, latitude, longitude):
        if id not in self.nodes:
            node = Node(id, latitude, longitude)
            self.nodes[id] = node
        return self.nodes[id]

    def get_node(self, id):
        return self.nodes.get(id)
    
    def reset(self):
        for node in self.nodes.values():
            node.reset()

def build_graph_from_osm(data, start_node_id=None):
    """
    Xây dựng đồ thị từ dữ liệu Overpass API JSON.
    Nếu cung cấp start_node_id thì sẽ gán luôn start_node trong Graph.
    """
    elements = data.get("elements", [])
    graph = Graph()

    for element in elements:
        if element["type"] == "node":
            node = graph.add_node(
                id=element["id"],
                latitude=element["lat"],
                longitude=element["lon"]
            )

            if start_node_id and node.id == start_node_id:
                graph.start_node = node

        elif element["type"] == "way":
            node_refs = element.get("nodes", [])
            if len(node_refs) < 2:
                continue

            for i in range(len(node_refs) - 1):
                node1 = graph.get_node(node_refs[i])
                node2 = graph.get_node(node_refs[i + 1])

                if node1 and node2:
                    node1.connect_to(node2)

    if start_node_id and not graph.start_node:
        raise ValueError("Start node was not found in the graph.")

    return graph
