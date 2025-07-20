# simulation.py

from graph import Graph
import heapq

class Simulation:
    def __init__(self, map_filename):
        self.map = Graph()
        self.map.load_from_file(map_filename)

    def find_shortest_path(self, start, end):
        # Dijkstra’s algorithm using a min-heap (priority queue)
        distances = {node: float('inf') for node in self.map.adjacency_list}
        previous = {node: None for node in self.map.adjacency_list}
        distances[start] = 0

        heap = [(0, start)]  # (distance, node)

        while heap:
            current_dist, current_node = heapq.heappop(heap)

            if current_node == end:
                break

            for neighbor, weight in self.map.adjacency_list.get(current_node, []):
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(heap, (distance, neighbor))

        # Reconstruct path
        path = []
        current = end
        while current:
            path.insert(0, current)
            current = previous[current]

        return path, distances[end]

    def run(self):
        print("Simulation started. (event-driven logic to be implemented)")
        print("City Map:")
        print(self.map)

        # Sample test run: find shortest route from 'Airport' to 'Suburbs'
        path, total_time = self.find_shortest_path("Airport", "Suburbs")
        print(f"Shortest path: {' -> '.join(path)}")
        print(f"Total travel time (adjusted for traffic): {total_time:.1f}")
