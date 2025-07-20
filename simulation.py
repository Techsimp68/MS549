# simulation.py

from graph import Graph
from car import Car
from rider import Rider
import heapq

class Simulation:
    def __init__(self, map_filename):
        self.map = Graph()
        self.map.load_from_file(map_filename)

        # Week 2 integrations
        self.cars = {}    # key = car_id, value = Car object
        self.riders = {}  # key = rider_id, value = Rider object

    def add_car(self, car_id, location):
        car = Car(car_id, location)
        self.cars[car_id] = car

    def add_rider(self, rider_id, start_location, destination):
        rider = Rider(rider_id, start_location, destination)
        self.riders[rider_id] = rider

    def find_shortest_path(self, start, end):
        distances = {node: float('inf') for node in self.map.adjacency_list}
        previous = {node: None for node in self.map.adjacency_list}
        distances[start] = 0
        heap = [(0, start)]

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
        print("Simulation started.")
        print("Loaded City Map:")
        print(self.map)

        # Demo: Add sample car and rider
        self.add_car("CAR001", ("Airport"))
        self.add_rider("RIDER_A", "Airport", "Suburbs")

        # Simulate route
        car = self.cars["CAR001"]
        rider = self.riders["RIDER_A"]
        path, time = self.find_shortest_path(rider.start_location, rider.destination)

        print(f"\nAssigning {rider.id} to {car.id}")
        print(f"Path: {' -> '.join(path)} | ETA: {time:.1f}")
