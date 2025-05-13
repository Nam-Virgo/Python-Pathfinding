# # algorithms/pathfinding_algorithm.py

import math

class PathfindingAlgorithm:
    def __init__(self):
        self.finished = False
        self.start_node = None
        self.end_node = None

    def start(self, start_node, end_node):
        """
        Khởi tạo trạng thái cho thuật toán tìm đường.
        """
        self.finished = False
        self.start_node = start_node
        self.end_node = end_node

    def next_step(self):
        """
        Tiến hành một bước trong thuật toán.
        Trả về danh sách các node đã được cập nhật.
        (Lớp con sẽ override hàm này.)
        """
        return []

class AStar(PathfindingAlgorithm):
    def __init__(self):
        super().__init__()
        self.open_list = []
        self.closed_list = []

    def start(self, start_node, end_node):
        super().start(start_node, end_node)
        self.open_list = [self.start_node]
        self.closed_list = []
        self.start_node.distance_from_start = 0
        self.start_node.distance_to_end = 0

    def next_step(self):
        if not self.open_list:
            self.finished = True
            return []

        updated_nodes = []
        current_node = min(self.open_list, key=lambda node: node.total_distance)
        self.open_list.remove(current_node)
        current_node.visited = True

        # Đánh dấu cạnh dẫn đến node hiện tại (nếu có)
        if current_node.referer:
            for edge in current_node.edges:
                if edge.get_other_node(current_node) == current_node.referer:
                    edge.visited = True
                    break

        # Nếu tìm thấy node đích
        if current_node.id == self.end_node.id:
            self.open_list = []
            self.finished = True
            return [current_node]

        # Xét các neighbor của current_node
        for neighbor_info in current_node.neighbors:
            neighbor = neighbor_info["node"]
            edge = neighbor_info["edge"]
            new_cost = current_node.distance_from_start + edge.weight

            if not neighbor.visited and not edge.visited:
                edge.visited = True
                neighbor.referer = current_node
                updated_nodes.append(neighbor)

            if neighbor in self.open_list:
                if neighbor.distance_from_start <= new_cost:
                    continue
            elif neighbor in self.closed_list:
                if neighbor.distance_from_start <= new_cost:
                    continue
                self.closed_list.remove(neighbor)

            self.open_list.append(neighbor)
            neighbor.distance_from_start = new_cost
            # Tính heuristic (khoảng cách Euclid đến end_node)
            neighbor.distance_to_end = math.hypot(
                neighbor.longitude - self.end_node.longitude,
                neighbor.latitude - self.end_node.latitude
            )
            neighbor.parent = current_node

        self.closed_list.append(current_node)
        return updated_nodes + [current_node]

class Dijkstra(PathfindingAlgorithm):
    def __init__(self):
        super().__init__()
        self.open_list = []
        self.closed_list = []

    def start(self, start_node, end_node):
        super().start(start_node, end_node)
        self.open_list = [self.start_node]
        self.closed_list = []
        self.start_node.distance_from_start = 0

    def next_step(self):
        if not self.open_list:
            self.finished = True
            return []
        updated_nodes = []
        # Chọn node có distance_from_start nhỏ nhất
        current_node = min(self.open_list, key=lambda node: node.distance_from_start)
        self.open_list.remove(current_node)
        current_node.visited = True
        # Đánh dấu cạnh dẫn đến node hiện tại (nếu có)
        if current_node.referer:
            for edge in current_node.edges:
                if edge.get_other_node(current_node) == current_node.referer:
                    edge.visited = True
                    break
        # Nếu tìm thấy node đích
        if current_node.id == self.end_node.id:
            self.open_list = []
            self.finished = True
            return [current_node]
        # Xét các neighbor của current_node
        for neighbor_info in current_node.neighbors:
            neighbor = neighbor_info["node"]
            edge = neighbor_info["edge"]
            new_cost = current_node.distance_from_start + edge.weight

            if not neighbor.visited and not edge.visited:
                edge.visited = True
                neighbor.referer = current_node
                updated_nodes.append(neighbor)

            if neighbor in self.open_list:
                if neighbor.distance_from_start <= new_cost:
                    continue
            elif neighbor in self.closed_list:
                if neighbor.distance_from_start <= new_cost:
                    continue
                self.closed_list.remove(neighbor)

            self.open_list.append(neighbor)
            neighbor.distance_from_start = new_cost
            neighbor.parent = current_node

        self.closed_list.append(current_node)
        return updated_nodes + [current_node]

class Greedy(PathfindingAlgorithm):
    def __init__(self):
        super().__init__()
        self.open_list = []
        self.closed_list = []

    def start(self, start_node, end_node):
        super().start(start_node, end_node)
        self.open_list = [self.start_node]
        self.closed_list = []
        self.start_node.distance_from_start = 0
        # Tính heuristic cho start_node
        if self.end_node:
            self.start_node.distance_to_end = math.hypot(
                self.start_node.longitude - self.end_node.longitude,
                self.start_node.latitude - self.end_node.latitude
            )

    def next_step(self):
        if not self.open_list:
            self.finished = True
            return []
        updated_nodes = []
        # Chọn node có distance_to_end nhỏ nhất
        current_node = min(self.open_list, key=lambda node: node.distance_to_end)
        self.open_list.remove(current_node)
        current_node.visited = True
        # Đánh dấu cạnh dẫn đến node hiện tại (nếu có)
        if current_node.referer:
            for edge in current_node.edges:
                if edge.get_other_node(current_node) == current_node.referer:
                    edge.visited = True
                    break
        # Nếu tìm thấy node đích
        if current_node.id == self.end_node.id:
            self.open_list = []
            self.finished = True
            return [current_node]
        # Xét các neighbor của current_node
        for neighbor_info in current_node.neighbors:
            neighbor = neighbor_info["node"]
            edge = neighbor_info["edge"]
            if not neighbor.visited and not edge.visited:
                edge.visited = True
                neighbor.referer = current_node
                updated_nodes.append(neighbor)
            if neighbor in self.open_list or neighbor in self.closed_list:
                continue
            # Thêm neighbor vào open list và tính heuristic
            self.open_list.append(neighbor)
            neighbor.distance_from_start = 0
            neighbor.parent = current_node
            neighbor.distance_to_end = math.hypot(
                neighbor.longitude - self.end_node.longitude,
                neighbor.latitude - self.end_node.latitude
            )
        self.closed_list.append(current_node)
        return updated_nodes + [current_node]

class BFS(PathfindingAlgorithm):
    def __init__(self):
        super().__init__()
        self.queue = []

    def start(self, start_node, end_node):
        super().start(start_node, end_node)
        self.queue = [self.start_node]
        self.start_node.distance_from_start = 0

    def next_step(self):
        if not self.queue:
            self.finished = True
            return []
        updated_nodes = []
        current_node = self.queue.pop(0)
        current_node.visited = True
        # Đánh dấu cạnh dẫn đến node hiện tại (nếu có)
        if current_node.referer:
            for edge in current_node.edges:
                if edge.get_other_node(current_node) == current_node.referer:
                    edge.visited = True
                    break
        # Nếu tìm thấy node đích
        if current_node.id == self.end_node.id:
            self.finished = True
            return [current_node]
        # Xét các neighbor của current_node
        for neighbor_info in current_node.neighbors:
            neighbor = neighbor_info["node"]
            edge = neighbor_info["edge"]
            if not neighbor.visited and not edge.visited:
                edge.visited = True
                neighbor.parent = current_node
                neighbor.visited = True
                self.queue.append(neighbor)
                updated_nodes.append(neighbor)
        return updated_nodes + [current_node]

class DFS(PathfindingAlgorithm):
    def __init__(self):
        super().__init__()
        self.stack = []

    def start(self, start_node, end_node):
        super().start(start_node, end_node)
        self.stack = [self.start_node]
        self.start_node.distance_from_start = 0

    def next_step(self):
        if not self.stack:
            self.finished = True
            return []
        updated_nodes = []
        current_node = self.stack.pop()
        current_node.visited = True
        # Đánh dấu cạnh dẫn đến node hiện tại (nếu có)
        if current_node.referer:
            for edge in current_node.edges:
                if edge.get_other_node(current_node) == current_node.referer:
                    edge.visited = True
                    break
        # Nếu tìm thấy node đích
        if current_node.id == self.end_node.id:
            self.finished = True
            return [current_node]
        # Xét các neighbor của current_node
        for neighbor_info in current_node.neighbors:
            neighbor = neighbor_info["node"]
            edge = neighbor_info["edge"]
            if not neighbor.visited and not edge.visited:
                edge.visited = True
                neighbor.parent = current_node
                neighbor.visited = True
                self.stack.append(neighbor)
                updated_nodes.append(neighbor)
        return updated_nodes + [current_node]
