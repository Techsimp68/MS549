from graph import Graph
from car import Car
from rider import Rider
from event import Event
import heapq


class Simulation:
    def __init__(self, map_filename):
        self.current_time = 0
        self.event_queue = []
        self.map = Graph()
        self.map.load_from_file(map_filename)
        self.cars = {}
        self.riders = {}

        #  Statistics tracking
        self.total_rides = 0
        self.total_wait_time = 0
        self.car_idle_times = {}
        self.last_car_available_time = {}
        self.ride_request_times = {}
        self.max_concurrent_riders = 0
        self.current_waiting_riders = 0

    def add_car(self, car_id, location):
        car = Car(car_id, location)
        self.cars[car_id] = car
        self.last_car_available_time[car_id] = self.current_time

    def add_rider(self, rider_id, start_location, destination):
        rider = Rider(rider_id, start_location, destination)
        self.riders[rider_id] = rider

    def schedule_event(self, time, event_type, data=None):
        event = Event(time, event_type, data)
        heapq.heappush(self.event_queue, event)

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
        print(self.map)

        #  DEMO setup: 1 car, 1 rider
        self.add_car("CAR001", "Airport")
        self.add_rider("RIDER_A", "Airport", "Suburbs")

        # Schedule the ride request
        self.schedule_event(1, "request_ride", {"rider_id": "RIDER_A"})

        # Main event loop
        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            if event.time != self.current_time:
                print(f"\n=== Advancing to time {event.time} ===")
            self.current_time = event.time
            print(f"Processing: {event}")
            self.handle_event(event)

        print("\nSimulation finished.")
        self.print_statistics()

    def handle_event(self, event):
        if event.event_type == "request_ride":
            rider_id = event.data["rider_id"]
            rider = self.riders[rider_id]
            self.ride_request_times[rider_id] = self.current_time
            self.current_waiting_riders += 1
            self.max_concurrent_riders = max(self.max_concurrent_riders, self.current_waiting_riders)

            available_car = next((c for c in self.cars.values() if c.status == "available"), None)

            if not available_car:
                print(f"No cars available for {rider_id}")
                return

            car_id = available_car.id
            if car_id in self.last_car_available_time:
                idle_time = self.current_time - self.last_car_available_time[car_id]
                self.car_idle_times[car_id] = self.car_idle_times.get(car_id, 0) + idle_time

            path, eta = self.find_shortest_path(available_car.location, rider.start_location)
            print(f"{available_car.id} heading to pick up {rider.id}: {path} (ETA {eta:.1f})")

            available_car.status = "en_route_to_pickup"
            available_car.destination = rider.start_location

            self.schedule_event(self.current_time + int(eta), "pickup_rider", {
                "car_id": available_car.id,
                "rider_id": rider_id
            })

        elif event.event_type == "pickup_rider":
            car = self.cars[event.data["car_id"]]
            rider = self.riders[event.data["rider_id"]]

            wait_time = self.current_time - self.ride_request_times[rider.id]
            self.total_wait_time += wait_time
            self.current_waiting_riders -= 1

            car.status = "en_route_to_destination"
            car.location = rider.start_location
            car.destination = rider.destination
            rider.status = "in_car"

            path, eta = self.find_shortest_path(rider.start_location, rider.destination)
            print(f"{car.id} picked up {rider.id}. Heading to {rider.destination} (ETA {eta:.1f})")

            self.schedule_event(self.current_time + int(eta), "dropoff_rider", {
                "car_id": car.id,
                "rider_id": rider.id
            })

        elif event.event_type == "dropoff_rider":
            car = self.cars[event.data["car_id"]]
            rider = self.riders[event.data["rider_id"]]

            car.status = "available"
            car.location = rider.destination
            car.destination = None
            rider.status = "completed"

            self.total_rides += 1
            self.last_car_available_time[car.id] = self.current_time

            print(f"{car.id} dropped off {rider.id} at {rider.destination}")

    def print_statistics(self):
        print("\n--- Simulation Summary ---")
        print(f"Total rides completed: {self.total_rides}")
        avg_wait = self.total_wait_time / self.total_rides if self.total_rides else 0
        print(f"Average wait time: {avg_wait:.2f} ticks")
        print(f"Max concurrent waiting riders: {self.max_concurrent_riders}")
        print("Idle time per car:")
        for car_id, idle in self.car_idle_times.items():
            print(f"  {car_id}: {idle:.1f} ticks")
