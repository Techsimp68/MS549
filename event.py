# event.py

class Event:
    def __init__(self, time, event_type, data=None):
        self.time = time
        self.event_type = event_type
        self.data = data or {}

    def __lt__(self, other):
        return self.time < other.time  # for heapq to sort by time

    def __str__(self):
        return f"[Time {self.time}] {self.event_type} -> {self.data}"
