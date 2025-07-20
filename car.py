# car.py

class Car:
    def __init__(self, car_id, location):
        self.id = car_id
        self.location = location  # Tuple (x, y)
        self.status = "available"
        self.destination = None

    def __str__(self):
        return f"Car {self.id} at {self.location} - Status: {self.status}"
