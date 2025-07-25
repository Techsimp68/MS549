# rider.py

class Rider:
    def __init__(self, rider_id, start_location, destination):
        self.id = rider_id
        self.start_location = start_location  # Tuple (x, y)
        self.destination = destination  # Tuple (x, y)
        self.status = "waiting"

    def __str__(self):
        return (f"Rider {self.id} at {self.start_location} "
                f"waiting for ride to {self.destination}")
